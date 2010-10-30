def reduce(keys, values, rereduce):
    if rereduce:
        return {
            "works": sum(v['works'] for v in values),
            "editions": sum(v['editions'] for v in values),
            "ebooks": sum(v['ebooks'] for v in values)
        }
    
    else:
        return {
           "works": sum(len(v['works']) for v in values),
           "editions": sum(len(v['editions']) for v in values),
           "ebooks": sum(len([e for e in v['editions'] if 'ia' in e]) for v in values)
        }
