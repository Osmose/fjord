#!/usr/bin/env python
import sys
import glob
import os

import polib
from pyexcel_xls import get_data, save_data


def main(argv):
    for filename in glob.glob('locale/*/LC_MESSAGES/django.po'):
        locale = filename.split('/')[1]
        print 'Translating %s...' % locale,
        pofile = polib.pofile(filename, encoding='UTF-8')

        def t(string):
            entity = pofile.find(string)
            if entity:
                return entity.msgstr
            else:
                return string

        xls_data = get_data(argv[0], encoding='UTF-8')
        sheet = xls_data['Sheet 1']

        def trans(row, string):
            row = sheet[row - 1]
            while len(row) < 3:
                row.append('')
            row[2] = string

        try:
            trans(5, t(u'How does %(product)s make you feel?') % {'product': t('Firefox')})
            trans(7, t(u'%(product)s makes me sad') % {'product': t('Firefox')})
            trans(8, t(u'%(product)s makes me happy') % {'product': t('Firefox')})
            trans(12, u'<span style="font-size:16px;">%(tohelp)s<br /><br />%(please)s</span>' % {
                'tohelp': t(u'To help us understand your input, we need more information.'),
                'please': t(u'Please describe your problem below and be as specific as you can. The content of your feedback will be public, so please be sure not to include personal information such as email address, passwords or phone number.'),
            })
            trans(14, u'<span style="font-size:16px;">%(tohelp)s<br /><br />%(please)s</span>' % {
                'tohelp': t(u'To help us understand your input, we need more information.'),
                'please': t(u'Please describe what you like. The content of your feedback will be public, so please be sure not to include personal information such as email address, passwords or phone number.'),
            })
            trans(16, u'<span style="font-size:16px;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;">%(feedback)s</span>' % {
                'feedback': t(u'If your feedback is related to a website, you can include it here:'),
            }),
            trans(20, u"""
            <div class="card thanks">
                <section>
                    <div class="part">%(yourfeedback)s</div>

                    <div class="part">
                        <h2>%(havingproblems)s</h2>
                        <p>%(gotoour)s</p>
                    </div>

                    <div class="part">
                        <h2>%(shapethe)s</h2>
                        <p>%(downloadthebuild)s</p>
                    </div>

                    <div class="part">
                        <h2>%(contributeto)s</h2>
                        <p>%(learnhow)s</p>
                    </div>

                    <div class="part" id="thanks-news">
                        <h2>%(findthelatest)s</h2>
                        <ul>
                            <li><a href="http://twitter.com/firefox" id="twitter"><span>%(twitter)s</span></a></li>
                            <li><a href="http://www.facebook.com/Firefox" id="facebook"><span>%(facebook)s</span></a></li>
                            <li><a href="http://planet.mozilla.org/" id="planet"><span>%(planetmozilla)s</span></a></li>
                        </ul>
                    </div>
                </section>
            </div>
            """ % {
                'yourfeedback': t(u'Your feedback will be used to create a better experience in future releases of %(product)s.') % {
                    'product': t(u'Firefox'),
                },
                'havingproblems': t(u'Having problems? Get help.'),
                'gotoour': t(u'Go to our support forum where you can <a href="%(url)s">get help and find answers</a>.') % {
                    'url': 'https://support.mozilla.org/questions/new?utm_source=input&utm_campaign=thankyou',
                },
                'shapethe': t(u'Shape the future of Firefox.'),
                'downloadthebuild': t(u'Download <a href="%(download_url)s">the Firefox build that is right for you</a>.') % {
                    'download_url': 'http://www.mozilla.org/firefox/channel',
                },
                'contributeto': t(u'Contribute to Mozilla.'),
                'learnhow': t(u'Learn how you can <a href="%(url)s">make %(product)s and Mozilla better</a>.') % {
                    'url': 'http://mozilla.org/contribute/',
                    'product': t(u'Firefox'),
                },
                'findthelatest': t(u'Find the latest news about %(product)s.') % {
                    'product': t(u'Firefox'),
                },
                'twitter': t(u'Twitter'),
                'facebook': t(u'Facebook'),
                'planetmozilla': t(u'Planet Mozilla'),
            })
            trans(127, t(u'Submit'))
            trans(32, t(u'This question is required.'))
            trans(34, t(u'This question is required.'))
            trans(111, t(u'There was an error on your page. Please correct any required fields and submit again.'))
            trans(112, t(u'Go to the first error'))

            save_data(os.path.join(argv[1], '%s.xls' % locale), xls_data, encoding='UTF-8')
        except (KeyError, ValueError):
            print 'Skipped'
        else:
            print ''


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
