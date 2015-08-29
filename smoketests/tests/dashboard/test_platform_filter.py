# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.dashboard import DashboardPage


class TestPlatformFilter(object):
    @pytest.mark.nondestructive
    def test_feedback_can_be_filtered_by_platform(self, mozwebqa):
        """Tests platform filtering in dashboard

        1. Verify that the selected platform is the only one to appear in the list and is selected
        2. Verify that the number of messages is less than the total messages
        3. Verify that the platform appears in the URL
        4. Verify that the platform for all messages on the first page of results is correct

        """
        dashboard_pg = DashboardPage(mozwebqa)

        dashboard_pg.go_to_dashboard_page()
        total_messages = dashboard_pg.total_message_count

        platforms = dashboard_pg.platform_filter.platforms
        platform_names = [platform.name for platform in platforms]

        assert len(platforms) > 0

        for name in platform_names[:2]:
            platform = dashboard_pg.platform_filter.platform(name)

            platform_name = platform.name
            platform_code = platform.code

            platform_count = platform.message_count
            assert total_messages > platform_count

            dashboard_pg.platform_filter.select_platform(platform_code)

            assert total_messages > dashboard_pg.total_message_count
            assert len(dashboard_pg.platform_filter.platforms) == 1
            assert dashboard_pg.platform_filter.selected_platform.name == platform_name
            assert dashboard_pg.platform_from_url == platform_code

            for message in dashboard_pg.messages:
                assert message.platform == platform_name

            dashboard_pg.platform_filter.unselect_platform(platform_code)
