import re
def map(doc, re_subject=re.compile("[, _]+")):
    def get_editions(work):
        editions = work.get('editions', [])
        for e in editions:
            doc = {'key': e['key']}
            if 'ocaid' in e:
                doc['ia'] = e['ocaid']
            yield doc
            
    def get_authors(work):
        return [a['author'] for a in work.get('authors', []) if 'author' in a]

    def _get_subject(subject, prefix):
        if isinstance(subject, basestring):
            key = prefix + re_subject.sub("_", subject.lower()).strip("_")
            return {"key": key, "name": subject}
    
    def get_subjects(work):
        subjects = [_get_subject(s, "subject:") for s in work.get("subjects", [])]
        places = [_get_subject(s, "place:") for s in work.get("subject_places", [])]
        people = [_get_subject(s, "person:") for s in work.get("subject_people", [])]
        times = [_get_subject(s, "time:") for s in work.get("subject_times", [])]
        return [s for s in subjects + places + people + times if s is not None]

    type = doc.get('type', {}).get('key')
    if type == "/type/work":
        work = doc
        authors = get_authors(work)
        subjects = get_subjects(work)
        editions = list(get_editions(work))
        
        xwork = {
            "works": [{"key": work['key']}],
            "subjects": subjects,
            "editions": editions,
        }
        
        yield work['key'], xwork        
        for a in authors:
            yield a['key'], xwork
            
        for e in editions:
            yield e['key'], dict(xwork, editions=[e])
        
        for s in subjects:
            yield s['key'], dict(xwork, subjects=[s])


del re
