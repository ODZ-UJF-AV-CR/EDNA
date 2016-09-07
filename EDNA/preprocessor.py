import models as md
import itertools

def check_visualization(measures, visual):
    meas_keys = []
    vis_keys = []
    for i in measures:
        for j in i.sensor.sensor_type.quantities.all():
            rec=j.pk,i.pk
            meas_keys.append(rec)
    for i in visual.quantities.all():
        vis_keys.append(i.pk)
    vis_num = len(vis_keys)
    meas_comb = list(itertools.combinations(meas_keys, vis_num))

    for i in meas_comb:
        active = md.PreprocessedData.objects.all()
        active = active.filter(visualization__pk = visual.pk)
        for j in measures:
            active = active.filter(measurements__pk = j.pk)
        if active:
            meas_comb.remove(i)

    for i in meas_comb:
        test_bool = True
        for j in vis_keys:
            for k in i:
                if not (k[0] in vis_keys):
                    test_bool = False
        if test_bool:
            new_preproc = md.PreprocessedData()
            new_preproc.visualization = visual
            new_preproc.save()
            for j in i:
                member = md.Measurement.objects.get(pk=j[1])
                new_preproc.measurements.add(member)
            new_preproc.calculate()
            new_preproc.save()

