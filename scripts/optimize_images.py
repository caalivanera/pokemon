"""
Image Optimization Script
Convert PNG sprites to WebP format for better performance
"""

import os
from pathlib import Path
from PIL import Image
import argparse
from typing import List, Tuple
import concurrent.futures


class ImageOptimizer:
    """Optimize Pokemon sprites for web performance"""
    
    def __init__(self, quality: int = 85):
        self.quality = quality
        self.stats = {
            'processed': 0,
            'failed': 0,
            'total_original_size': 0,
            'total_optimized_size': 0
        }
    
    def convert_to_webp(self, input_path: str, output_path: str = None,
                       keep_original: bool = True) -> Tuple[bool, str]:
        """
        Convert a single image to WebP format
        
        Args:
            input_path: Path to input image
            output_path: Path for output (auto-generated if None)
            keep_original: Keep original file after conversion
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Open image
            img = Image.open(input_path)
            
            # Generate output path if not provided
            if output_path is None:
                output_path = str(input_path).rsplit('.', 1)[0] + '.webp'
            
            # Get original size
            original_size = os.path.getsize(input_path)
            
            # Convert and save as WebP
            img.save(
                output_path,
                'webp',
                quality=self.quality,
                method=6  # Best compression
            )
            
            # Get optimized size
            optimized_size = os.path.getsize(output_path)
            
            # Update stats
            self.stats['processed'] += 1
            self.stats['total_original_size'] += original_size
            self.stats['total_optimized_size'] += optimized_size
            
            # Calculate savings
            savings = ((original_size - optimized_size) / original_size) * 100
            
            # Remove original if requested
            if not keep_original and input_path != output_path:
                os.remove(input_path)
            
            return True, (f"✅ {Path(input_path).name}: "
                         f"{original_size/1024:.1f}KB → "
                         f"{optimized_size/1024:.1f}KB "
                         f"({savings:.1f}% savings)")
        
        except Exception as e:
            self.stats['failed'] += 1
            return False, f"❌ {Path(input_path).name}: {str(e)}"
    
    def optimize_directory(self, directory: str, 
                          recursive: bool = True,
                          file_extensions: List[str] = None,
                          keep_original: bool = True,
                          max_workers: int = 4) -> None:
        """
        Optimize all images in a directory
        
        Args:
            directory: Path to directory
            recursive: Process subdirectories
            file_extensions: List of extensions to process
            keep_original: Keep original files
            max_workers: Number of parallel workers
        """
        if file_extensions is None:
            file_extensions = ['.png', '.jpg', '.jpeg']
        
        # Find all images
        dir_path = Path(directory)
        
        if recursive:
            image_files = []
            for ext in file_extensions:
                image_files.extend(dir_path.rglob(f'*{ext}'))
        else:
            image_files = []
            for ext in file_extensions:
                image_files.extend(dir_path.glob(f'*{ext}'))
        
        if not image_files:
            print(f"No images found in {directory}")
            return
        
        print(f"Found {len(image_files)} images to optimize...")
        print(f"Using {max_workers} parallel workers")
        print("-" * 60)
        
        # Process images in parallel
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers
        ) as executor:
            futures = {
                executor.submit(
                    self.convert_to_webp,
                    str(img_path),
                    None,
                    keep_original
                ): img_path
                for img_path in image_files
            }
            
            for future in concurrent.futures.as_completed(futures):
                success, message = future.result()
                print(message)
        
        self.print_stats()
    
    def print_stats(self):
        """Print optimization statistics"""
        print("\n" + "=" * 60)
        print("OPTIMIZATION SUMMARY")
        print("=" * 60)
        print(f"Processed: {self.stats['processed']} images")
        print(f"Failed: {self.stats['failed']} images")
        
        if self.stats['processed'] > 0:
            orig_mb = self.stats['total_original_size'] / (1024 * 1024)
            opt_mb = self.stats['total_optimized_size'] / (1024 * 1024)
            savings = ((self.stats['total_original_size'] - 
                       self.stats['total_optimized_size']) / 
                       self.stats['total_original_size']) * 100
            
            print(f"\nOriginal Total Size: {orig_mb:.2f} MB")
            print(f"Optimized Total Size: {opt_mb:.2f} MB")
            print(f"Total Savings: {savings:.1f}% "
                  f"({orig_mb - opt_mb:.2f} MB)")
            print(f"Average per file: "
                  f"{(orig_mb - opt_mb) / self.stats['processed']:.2f} MB")
        
        print("=" * 60)
    
    def optimize_pokemon_sprites(self, assets_dir: str = "assets"):
        """Optimize all Pokemon sprites"""
        assets_path = Path(assets_dir)
        
        print("🎨 Starting Pokemon Sprite Optimization")
        print("=" * 60)
        
        # Optimize different sprite categories
        directories = {
            'Static Sprites': assets_path / 'sprites' / 'base',
            'Shiny Sprites': assets_path / 'sprites' / 'shiny',
            'Animated Sprites': assets_path / 'sprites' / 'animated',
            'Icons': assets_path / 'icons'
        }
        
        for category, directory in directories.items():
            if directory.exists():
                print(f"\n📁 Processing {category}...")
                print("-" * 60)
                self.optimize_directory(
                    str(directory),
                    recursive=True,
                    keep_original=True
                )
            else:
                print(f"⚠️ {category} directory not found: {directory}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Optimize Pokemon sprite images"
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='assets',
        help='Directory to optimize (default: assets)'
    )
    
    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=85,
        help='WebP quality (1-100, default: 85)'
    )
    
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Do not process subdirectories'
    )
    
    parser.add_argument(
        '--delete-originals',
        action='store_true',
        help='Delete original files after conversion'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )
    
    parser.add_argument(
        '--sprites-only',
        action='store_true',
        help='Only optimize Pokemon sprites (assets/sprites)'
    )
    
    args = parser.parse_args()
    
    # Create optimizer
    optimizer = ImageOptimizer(quality=args.quality)
    
    # Run optimization
    if args.sprites_only:
        optimizer.optimize_pokemon_sprites(args.directory)
    else:
        optimizer.optimize_directory(
            args.directory,
            recursive=not args.no_recursive,
            keep_original=not args.delete_originals,
            max_workers=args.workers
        )


if __name__ == "__main__":
    main()
