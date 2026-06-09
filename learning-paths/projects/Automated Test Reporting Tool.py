import xml.etree.ElementTree as ET
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

class TestReportAnalyzer:
    def __init__(self, xml_path):
        self.xml_path = xml_path
        self.df = self.parse_pytest_xml()
    
    def parse_pytest_xml(self):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        
        test_cases = []
        for testcase in root.findall('.//testcase'):
            case_data = {
                'name': testcase.get('name'),
                'classname': testcase.get('classname'),
                'time': float(testcase.get('time')),
                'status': 'passed' if not testcase.findall('*') else 'failed'
            }
            test_cases.append(case_data)
        
        return pd.DataFrame(test_cases)
    
    def generate_dashboard(self):
        # Execution Summary
        summary = self.df['status'].value_counts().reset_index()
        summary.columns = ['Status', 'Count']
        
        # Duration Analysis
        fig = px.histogram(self.df, x='time', nbins=20, 
                          title='Test Execution Time Distribution')
        fig.write_html('duration_distribution.html')
        
        # Failure Analysis
        if 'failed' in summary['Status'].values:
            failed_tests = self.df[self.df['status'] == 'failed']
            failure_report = failed_tests.groupby('classname').size().reset_index(name='failures')
            failure_report.to_csv('failure_analysis.csv', index=False)
        
        # Generate Markdown Report
        with open('test_report.md', 'w') as f:
            f.write(f"# Test Execution Report\n\n")
            f.write(f"**Total Tests:** {len(self.df)}\n")
            f.write(f"**Pass Rate:** {summary.loc[summary['Status']=='passed', 'Count'].values[0]/len(self.df):.2%}\n")
            f.write("\n## Duration Distribution\n")
            f.write("![Duration Histogram](duration_distribution.html)\n")

if __name__ == "__main__":
    analyzer = TestReportAnalyzer('test_results.xml')
    analyzer.generate_dashboard()
