"""
Implement the command-line tool interface.
"""
import argparse
import sys
from diff_cover.diff_reporter import GitDiffReporter
from diff_cover.coverage_reporter import XmlCoverageReporter
from diff_cover.report_generator import HtmlReportGenerator, StringReportGenerator
from lxml import etree

DESCRIPTION = ""
GIT_BRANCH_HELP = ""
COVERAGE_XML_HELP = ""
HTML_REPORT_HELP = ""

def parse_args(argv):
    """
    Parse command line arguments, returning a dict of 
    valid options:

        {
            'git_branch': BRANCH,
            'coverage_xml': COVERAGE_XML,
            'html_report': None | HTML_REPORT
        }

    where `BRANCH` is the (string) name of the git branch to compare,
    `COVERAGE_XML` is a path, and `HTML_REPORT` is a path.

    The path strings may or may not exist.
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--git-branch', type=str, default='master',
                        help=GIT_BRANCH_HELP)
    parser.add_argument('--coverage-xml', type=str, default='',
                        help=COVERAGE_XML_HELP, required=True)
    parser.add_argument('--html-report', type=str, default='',
                        help=HTML_REPORT_HELP)

    return vars(parser.parse_args(argv))

def generate_report(coverage_xml=None, git_branch=None, html_report=None):
    """
    Generate the diff coverage report, using kwargs from `parse_args()`.
    """
    
    diff = GitDiffReporter(git_branch)
    coverage = XmlCoverageReporter(etree.parse(coverage_xml))

    # Build a report generator
    if html_report is not None:
        reporter = HtmlReportGenerator(coverage, diff)
        output_file = open(html_report, "w")
    else:
        reporter = StringReportGenerator(coverage, diff)
        output_file = sys.stdout

    # Generate the report
    reporter.generate_report(output_file)
