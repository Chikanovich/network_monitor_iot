import time
from datetime import datetime, timedelta

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

import plotly.offline as opy
import plotly.graph_objs as go
# import plotly.figure_factory as ff
from plotly.tools import FigureFactory as ff

from monitor.models import NetworkUsage


class MainPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        time_threshold = datetime.now() - timedelta(days=1)

        # date_created is column in db
        # __lt (less than) is field lookup. Field lookups are defined by double underscore
        # this line translates to: select * from monitor_networkusage where date_created > time_threshold
        # list executes query on the database
        data = list(NetworkUsage.objects.filter(
            date_created__gt=time_threshold))

        # endgoal is array of dict(Task='ip', Start='', Finish='')

        output = []
        for nu in data:
            # filter(lambda x: x.ip_address == nu.ip_address)
            existing_items = [
                x for x in output if x['Task'] == nu.ip_address]

            if (len(existing_items) > 0):
                # list is not empty
                last_el = existing_items[-1]

                diff_in_seconds = (nu.date_created -
                                   last_el['Finish']).total_seconds()
                diff_in_minutes = divmod(diff_in_seconds, 60)[0]

                if (diff_in_minutes <= 2):
                    # threshold is fine, just change last element finish time
                    last_el['Finish'] = nu.date_created
                else:
                    output.append(dict(Task=nu.ip_address, Start=nu.date_created,
                                       Finish=nu.date_created + timedelta(minutes=1)))
            else:
                # list is empty
                output.append(
                    dict(Task=nu.ip_address, Start=nu.date_created, Finish=nu.date_created + timedelta(minutes=1)))

        context = super(MainPage, self).get_context_data(**kwargs)

        gantt = ff.create_gantt(output, group_tasks=True)
        div = opy.plot(gantt, auto_open=False, output_type='div')

        context['gantt'] = div

        return context

        # return render(
        #     request,
        #     'index.html',
        #     {

        #     }
        # )
