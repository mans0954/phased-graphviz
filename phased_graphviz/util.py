

def parse_phases(s, min_phase, max_phase):
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    if s in ('', '-'):
        return set(range(min_phase, max_phase+1))
    phases = set()
    for phase_range in s.split(','):
        if '-' in phase_range:
            p_min, p_max = phase_range.split('-')
            p_min = int(p_min.strip()) if p_min.strip() else None
            p_max = int(p_max.strip()) if p_max.strip() else None
            if p_min is None:
                p_min = min(min_phase, p_max)
            if p_max is None:
                p_max = max(max_phase, p_min)
            phases |= set(range(p_min, p_max+1))
        elif phase_range:
            phases.add(int(phase_range.strip()))
    return phases

def test_phases():
    assert parse_phases("1-", 1, 2) == {1, 2}, parse_phases("1-", 1, 2)
    assert parse_phases("1-4", 1, 2) == {1, 2, 3, 4}, parse_phases("1-4", 1, 2)
    assert parse_phases("-4", 1, 2) == {1, 2, 3, 4}, parse_phases("-4", 1, 2)
    assert parse_phases("-1", 0, 2) == {0, 1}, parse_phases("-1", 0, 2)
    assert parse_phases("2-", 0, 0) == {2}, parse_phases("2-", 0, 0)
