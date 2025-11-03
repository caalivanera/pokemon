"""
Advanced Export System
Provides multiple export formats and customization options
"""

import streamlit as st
import pandas as pd
import json
import csv
from pathlib import Path
from typing import List, Dict, Optional
from io import BytesIO, StringIO
import zipfile
from datetime import datetime


class AdvancedExporter:
    """Advanced export system with multiple formats and options"""
    
    def __init__(self):
        """Initialize the exporter"""
        self.supported_formats = ['CSV', 'JSON', 'Excel', 'Markdown', 'HTML']
        
    def export_to_csv(self, df: pd.DataFrame, filename: str = "export.csv") -> BytesIO:
        """Export DataFrame to CSV"""
        output = BytesIO()
        df.to_csv(output, index=False, encoding='utf-8')
        output.seek(0)
        return output
    
    def export_to_json(self, df: pd.DataFrame, 
                       filename: str = "export.json",
                       orient: str = 'records') -> BytesIO:
        """Export DataFrame to JSON"""
        output = BytesIO()
        json_str = df.to_json(orient=orient, indent=2)
        output.write(json_str.encode('utf-8'))
        output.seek(0)
        return output
    
    def export_to_excel(self, df: pd.DataFrame, 
                        filename: str = "export.xlsx",
                        sheet_name: str = "Data") -> BytesIO:
        """Export DataFrame to Excel"""
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        output.seek(0)
        return output
    
    def export_to_markdown(self, df: pd.DataFrame, 
                          filename: str = "export.md") -> BytesIO:
        """Export DataFrame to Markdown table"""
        output = BytesIO()
        markdown_str = df.to_markdown(index=False)
        output.write(markdown_str.encode('utf-8'))
        output.seek(0)
        return output
    
    def export_to_html(self, df: pd.DataFrame, 
                       filename: str = "export.html",
                       title: str = "Pokemon Data Export") -> BytesIO:
        """Export DataFrame to HTML with styling"""
        output = BytesIO()
        
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-top: 20px;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .footer {{
            margin-top: 20px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    {df.to_html(index=False, classes='data-table', border=0)}
    <div class="footer">
        <p>Pokemon National Dex Dashboard v5.4.0</p>
        <p>Total Records: {len(df)}</p>
    </div>
</body>
</html>
"""
        output.write(html_template.encode('utf-8'))
        output.seek(0)
        return output
    
    def create_batch_export(self, data_dict: Dict[str, pd.DataFrame],
                           format_type: str = 'csv') -> BytesIO:
        """Create a zip file with multiple exports"""
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for name, df in data_dict.items():
                # Create individual export
                if format_type.lower() == 'csv':
                    file_data = self.export_to_csv(df)
                    filename = f"{name}.csv"
                elif format_type.lower() == 'json':
                    file_data = self.export_to_json(df)
                    filename = f"{name}.json"
                elif format_type.lower() == 'excel':
                    file_data = self.export_to_excel(df, sheet_name=name)
                    filename = f"{name}.xlsx"
                else:
                    continue
                
                # Add to zip
                zip_file.writestr(filename, file_data.getvalue())
        
        zip_buffer.seek(0)
        return zip_buffer
    
    def render_export_interface(self, df: pd.DataFrame, 
                                data_name: str = "pokemon_data"):
        """Render the export interface in Streamlit"""
        st.markdown("### 📤 Export Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            export_format = st.selectbox(
                "Export Format:",
                self.supported_formats
            )
        
        with col2:
            include_index = st.checkbox("Include Row Index", value=False)
        
        with col3:
            custom_filename = st.text_input(
                "Filename (without extension):",
                value=data_name
            )
        
        # Format-specific options
        if export_format == 'JSON':
            json_orient = st.selectbox(
                "JSON Orientation:",
                ['records', 'columns', 'index', 'values'],
                help="How to structure the JSON output"
            )
        
        if export_format == 'Excel':
            sheet_name = st.text_input("Sheet Name:", value="Sheet1")
        
        if export_format == 'HTML':
            html_title = st.text_input("HTML Title:", value="Pokemon Data Export")
        
        # Column selection
        st.markdown("**Select Columns to Export:**")
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect(
            "Columns:",
            all_columns,
            default=all_columns
        )
        
        if not selected_columns:
            st.warning("Please select at least one column to export")
            return
        
        # Filter data
        filtered_df = df[selected_columns].copy()
        
        # Show preview
        with st.expander("📊 Preview Export Data"):
            st.dataframe(filtered_df.head(10))
            st.info(f"Total rows: {len(filtered_df)} | Total columns: {len(selected_columns)}")
        
        # Export button
        if st.button("🚀 Generate Export", type="primary"):
            try:
                # Generate export based on format
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                if export_format == 'CSV':
                    file_data = self.export_to_csv(filtered_df)
                    filename = f"{custom_filename}_{timestamp}.csv"
                    mime_type = "text/csv"
                
                elif export_format == 'JSON':
                    file_data = self.export_to_json(filtered_df, orient=json_orient)
                    filename = f"{custom_filename}_{timestamp}.json"
                    mime_type = "application/json"
                
                elif export_format == 'Excel':
                    file_data = self.export_to_excel(
                        filtered_df, 
                        sheet_name=sheet_name
                    )
                    filename = f"{custom_filename}_{timestamp}.xlsx"
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                elif export_format == 'Markdown':
                    file_data = self.export_to_markdown(filtered_df)
                    filename = f"{custom_filename}_{timestamp}.md"
                    mime_type = "text/markdown"
                
                elif export_format == 'HTML':
                    file_data = self.export_to_html(filtered_df, title=html_title)
                    filename = f"{custom_filename}_{timestamp}.html"
                    mime_type = "text/html"
                
                else:
                    st.error("Unsupported format")
                    return
                
                # Download button
                st.success("✅ Export generated successfully!")
                st.download_button(
                    label=f"📥 Download {export_format}",
                    data=file_data,
                    file_name=filename,
                    mime=mime_type
                )
                
            except Exception as e:
                st.error(f"Export failed: {e}")
    
    def render_batch_export_interface(self, data_dict: Dict[str, pd.DataFrame]):
        """Render batch export interface"""
        st.markdown("### 📦 Batch Export")
        st.info("Export multiple datasets as a single ZIP file")
        
        # Show available datasets
        st.markdown("**Available Datasets:**")
        for name, df in data_dict.items():
            st.markdown(f"- **{name}**: {len(df)} rows, {len(df.columns)} columns")
        
        # Select format
        batch_format = st.selectbox(
            "Export Format for all files:",
            ['CSV', 'JSON', 'Excel']
        )
        
        if st.button("🚀 Generate Batch Export", type="primary"):
            try:
                zip_data = self.create_batch_export(data_dict, batch_format.lower())
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"pokemon_batch_export_{timestamp}.zip"
                
                st.success("✅ Batch export generated successfully!")
                st.download_button(
                    label="📥 Download ZIP",
                    data=zip_data,
                    file_name=filename,
                    mime="application/zip"
                )
            except Exception as e:
                st.error(f"Batch export failed: {e}")


def main():
    """Main function for standalone testing"""
    st.set_page_config(page_title="Advanced Export System", layout="wide")
    st.title("📤 Advanced Export System")
    
    # Sample data
    sample_data = pd.DataFrame({
        'name': ['Bulbasaur', 'Charmander', 'Squirtle'],
        'type1': ['Grass', 'Fire', 'Water'],
        'hp': [45, 39, 44],
        'attack': [49, 52, 48]
    })
    
    exporter = AdvancedExporter()
    exporter.render_export_interface(sample_data, "sample_pokemon")


if __name__ == "__main__":
    main()
