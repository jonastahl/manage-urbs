import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from projects.api.helper import get_project
from projects.models import Site, Commodity, Process, ProcessCommodity, SupIm, Demand


@login_required
@require_POST
def trigger_simulation(request, project_name):
    project = get_project(request.user, project_name)
    sites = Site.objects.filter(project=project)
    commodities = Commodity.objects.filter(site__in=sites)
    supims = SupIm.objects.filter(commodity__in=commodities)
    demands = Demand.objects.filter(commodity__in=commodities)
    timesteps = min(min(map(lambda supim: len(supim.steps), supims)),
                    min(map(lambda demand: len(demand.steps), demands)))

    data = {
        "c_timesteps": timesteps,
        "global": {
            "CO2 limit": project.co2limit,
            "Cost limit": project.costlimit
        },
        "site": {
            site.name: {
                "area": site.area,
                "commodity": {
                    commodity.name: {
                        "Type": commodity.get_com_type_label(),
                        "price": commodity.price,
                        "max": None if commodity.max is None else commodity.max if commodity.max >= 0 else "inf",
                        "maxperhour": None if commodity.maxperhour is None else commodity.maxperhour if commodity.maxperhour >= 0 else "inf",
                    }
                    for commodity in Commodity.objects.filter(site=site)
                },
                "process": {
                    process.name: {
                        "inst-cap": process.instcap,
                        "cap-lo": process.caplo,
                        "cap-up": process.capup,
                        "max-grad": "inf" if process.maxgrad < 0 else process.maxgrad,
                        "min-fraction": process.minfraction,
                        "inv-cost": process.invcost,
                        "fix-cost": process.fixcost,
                        "var-cost": process.varcost,
                        "wacc": process.wacc,
                        "depreciation": process.depreciation,
                        "area-per-cap": process.areapercap,
                        "commodity": {
                            proccom.commodity.name: {
                                "Direction": proccom.get_direction_type_label(),
                                "ratio": proccom.ratio,
                                "ratio-min": proccom.ratiomin,
                            }
                            for proccom in ProcessCommodity.objects.filter(process=process)
                        }
                    }
                    for process in Process.objects.filter(site=site)
                }
            }
            for site in sites
        },
        "supim": {
            site.name: {
                commodity.name: supim.steps
                for commodity in Commodity.objects.filter(site=site)
                for supim in SupIm.objects.filter(commodity=commodity)
            }
            for site in sites
        },
        "demand": {
            site.name: {
                commodity.name: demand.steps
                for commodity in Commodity.objects.filter(site=site)
                for demand in Demand.objects.filter(commodity=commodity)
            }
            for site in sites
        },
    }

    print(requests.post("http://localhost:5000/simulate", json=remove_none(data)).json())

    return JsonResponse({'detail': 'Triggered simulation'})


def remove_none(d):
    if isinstance(d, dict):
        return {k: remove_none(v) for k, v in d.items() if v is not None}
    elif isinstance(d, list):
        return [remove_none(v) for v in d if v is not None]
    else:
        return d
