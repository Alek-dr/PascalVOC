from itertools import combinations

from pascal import annotation_from_xml


def test_obj_filter(valid_annotations):
    for ann_sample in valid_annotations:
        ann_file = ann_sample.get("file")
        n_objects = ann_sample.get("n_objects")
        obj_info = ann_sample.get("obj_info")
        obj_counts = obj_info.get("count")
        n_names = len(obj_info.get("names"))
        for i in range(1, n_names + 1):
            for comb in combinations(obj_info.get("names"), i):
                n_filter = sum([obj_counts.get(k) for k in comb])
                ann = annotation_from_xml(ann_file)
                assert len(ann) == n_objects
                ann.filter_objects(comb)
                assert len(ann) == n_objects - n_filter
