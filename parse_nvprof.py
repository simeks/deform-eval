import re, sys

# Header: 
# 0,     1,        2,     3,      4,    5,    6,    7
# "Type","Time(%)","Time","Calls","Avg","Min","Max","Name"
# ,%,ns,,ns,ns,ns,

def convert_unit_to_ms(units, sample):
    out = sample
    for i in range(1, 7):
        s = float(sample[i])
        if units[i] == 'ns':
            s = s / 1000000
        elif units[i] == 'us':
            s = s / 1000
        elif units[i] == 's':
            s = s * 1000
        out[i] = s
    return out

def pretty_gpu_name(name):
    if re.match('"reduce_total_energy.*$', name):
        return 'total_energy'
    if re.match('"apply_displacement.*$', name):
        return 'apply_displacement'
    if re.match('"void cost_function_kernel.*$', name):
        return 'unary_function'
    if re.match('"regularizer_kernel.*$', name):
        return 'binary_function'
    return name

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: {} <input log> <output csv>'.format(sys.argv[0]))
        sys.exit(1)

    file = sys.argv[1]
    out = sys.argv[2]

    data = {}
    with open(file, 'r') as f:
        lines = f.readlines()
        
        i = 0
        while i < len(lines):
            m = re.match('==\d+==\s*Profiling result:$', lines[i])
            if m:
                i += 1
                if re.match('No kernels were profiled.$', lines[i]):
                    i += 1
                    continue
            
                cols = lines[i].strip().split(',')
                i += 1
                units = lines[i].strip().split(',')
                i += 1

                while lines[i].startswith('"GPU activities"'):
                    sample = convert_unit_to_ms(units, lines[i].strip().split(','))
                    sample[7] = pretty_gpu_name(sample[7])

                    if sample[7] in data:
                        data[sample[7]].append(sample)
                    else:
                        data[sample[7]] = [sample]

                    i += 1


            m = re.match('==\d+==\s*Range "([a-z_]*)"$', lines[i])
            if m:
                name = m.group(1)
                i += 1

                cols = lines[i].strip().split(',')
                i += 1
                units = lines[i].strip().split(',')
                i += 1
                sample = convert_unit_to_ms(units, lines[i].strip().split(','))

                if name in data:
                    data[name].append(sample)
                else:
                    data[name] = [sample]
            else:
                i += 1

    # Aggregate ranges

    ranges = []
    for name, samples in data.items():
        total_ms = 0
        calls = 0
        min_ms = None
        max_ms = None

        for s in samples:
            total_ms += float(s[2])
            calls += float(s[3])
            
            if min_ms:
                min_ms = min(min_ms, float(s[5]))
            else:
                min_ms = float(s[5])
                
            if max_ms:
                max_ms = max(max_ms, float(s[6]))
            else:
                max_ms = float(s[6])

        avg_ms = total_ms / calls

        ranges.append((name.replace('"',''), total_ms, calls, avg_ms, min_ms, max_ms))

    with open(out, 'w') as f:
        f.write('name,total,calls,avg,min,max\n')
        for r in ranges:
            f.write('{},{},{},{},{},{}\n'.format(*r))
