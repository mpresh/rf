import optparse
import unittest
import urllib

from BeautifulSoup import BeautifulSoup

#
# Constants
#
WEBROOTS = dict(local = 'http://www.demo.com:8000/',
                qa = 'http://qa.ripplefunction.com/',
                prod = 'http://www.ripplefunction.com/')

WEBROOT =  WEBROOTS.get('local') # Overridden by main()

#
# Base test case classes
#
class RippleTestCase(unittest.TestCase):
    """ Base test class for all tests. Contains setup and teardown code that
        is used by all test cases. Also contains methods for parsing HTML."""

    def setUp(self):
        """ Code that sets up whatever needs to be setup for the test. """
        pass

    def tearDown(self):
        """ Code that tears down and/or cleans up whatever was setup for the test. """
        pass

    def get_page(self, url, **get_vars):
        """ Gets page contents given a URL path using GET. """
        stream = urllib.urlopen(WEBROOT + '?' + urllib.urlencode(get_vars))
        page = stream.read()
        stream.close()
        return BeautifulSoup(page)

    def post_to_page(self, url, **post_vars):
        """ Gets page contents given a URL path using POST. """
        stream = urllib.urlopen(WEBROOT, urllib.urlencode(post_vars))
        page = stream.read()
        stream.close()
        return BeautifulSoup(page)

#
# Front page tests 
#
class FrontpageTestCase(RippleTestCase):
    """ Test the basic content and features of the front page. """

    def test_basic_contents(self):
        """ Basic front page test. """

        main_page = self.get_page('/')
        self.assertTrue('RippleFunction' in main_page.title.string, 
                        "Title must contain RippleFunction")
        

###########################################################
# Run unit tests
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", metavar = 'TARGET',
                      help = ("set target host against which the tests should be run; "
                              "presets include local [default], qa and prod."))
    parser.add_option("-c", "--testcase", metavar = 'TEST',
                      help = "run a specific test")

    (options, args) = parser.parse_args()
    target = WEBROOTS.get(options.target) or options.target or WEBROOT

    print
    print "Test target host set to: %s" % target
    print

    additional_args = ['test.py', '--verbose']
    if options.testcase:
        additional_args += options.testcase

    unittest.main(argv = additional_args)
