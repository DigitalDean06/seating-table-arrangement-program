import json
from copy import deepcopy
from random import randint


layout_format = None
layout = []
conds = []
table = []

def get_output(content, n=2):
    return f'{" " * n}{content}'


def output(content, n=2, end=None):
    print(get_output(content, n=n), end=end)


def get_input(content, n=2):
    return input(get_output(content, n=n))


def output_command(command, description):
    output(f'$ %-40s{description}'%command)


def count():
    global layout
    counter = 0
    for row in layout:
        for seat in row:
            counter += 1 if seat == 0 else 0
    return counter


def get_nums(n):
    return list(range(1, 1 + count()))


def get_num(nums):
    i = randint(0, len(nums) - 1)
    num = nums[i]
    del nums[i]
    return num
    

def get_coord(num):
    global layout
    global table
    for i in range(len(table)):
        for j in range(len(table[i])):
            if layout[i][j] is not None and table[i][j] == num:
                return [i, j]
    return None


def get_adj_coords(coord):
    global layout
    adj_coords = []
    for i in range(-1, 1 + 1):
        for j in range(-1, 1 + 1):
            if i == j == 0:
                continue
            x = coord[0] + i
            y = coord[1] + j
            if x < 0 or y < 0 or x >= len(layout) or y >= len(layout[x]) or layout[x][y] is None:
                continue
            adj_coords.append([x, y])
    return adj_coords


def get_rem_coords(coord):
    global layout
    adj_coords = get_adj_coords(coord)
    rem_coords = []
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            if [i, j] not in adj_coords and [i, j] != coord and layout[i][j] is not None:
                rem_coords.append([i, j])
    return rem_coords


def get_row_coords(n):
    global layout
    coords = []
    for i in range(len(layout[n])):
        if layout[n][i] == 0:
            coords.append([n, i])
    return coords


def get_row_coords_neg(n):
    global layout
    coords = []
    for i in range(len(layout)):
        if i == n:
            continue
        for j in range(len(layout[i])):
            if layout[i][j] == 0:
                coords.append([i, j])
    return coords


def get_col_coords(n):
    global layout
    coords = []
    for i in range(len(layout)):
        if layout[i][n] == 0:
            coords.append([i, n])
    return coords


def get_col_coords_neg(n):
    global layout
    coords = []
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            if j == n:
                continue
            if layout[i][j] == 0:
                coords.append([i, n])
    return coords


def valid(cond):
    cond_type = cond.get('type')
    data_1 = cond.get('data_1')
    data_2 = cond.get('data_2')
    if cond_type == 'a' and get_coord(data_1) not in get_adj_coords(get_coord(data_2)):
        return False
    elif cond_type == 'b' and get_coord(data_1) in get_adj_coords(get_coord(data_2)):
        return False
    elif cond_type == 'c' and get_coord(data_1)[0] != data_2:
        return False
    elif cond_type == 'd' and get_coord(data_1)[0] == data_2:
        return False
    elif cond_type == 'e' and get_coord(data_1)[1] != data_2:
        return False
    elif cond_type == 'f' and get_coord(data_1)[1] == data_2:
        return False
    return True


def swap(coord1, coord2):
    temp = table[coord1[0]][coord1[1]]
    table[coord1[0]][coord1[1]] = table[coord2[0]][coord2[1]]
    table[coord2[0]][coord2[1]] = temp


def valid_table():
    global conds
    b = True
    counter = 0
    while b and counter <= 1000:
        b = False
        counter += 1
        for cond in conds:
            if not valid(cond):
                b = True
                cond_type = cond.get('type')
                data_1 = cond.get('data_1')
                data_2 = cond.get('data_2')
                if cond_type == 'a':    
                    i = randint(0, 1)
                    targets = get_adj_coords(get_coord(data_1 if i == 0 else data_2))
                    if not targets:
                        counter = 1001
                        break
                    target = targets[randint(0, len(targets) - 1)]
                    swap(get_coord(data_2 if i == 0 else data_1), target)
                elif cond_type == 'b':
                    i = randint(0, 1)
                    targets = get_rem_coords(get_coord(data_1 if i == 0 else data_2))
                    if not targets:
                        counter = 1001
                        break
                    target = targets[randint(0, len(targets) - 1)]
                    swap(get_coord(data_2 if i == 0 else data_1), target)
                elif cond_type == 'c':
                    targets = get_row_coords(get_coord(data_1)[0])
                    if not targets:
                        counter = 1001
                        break
                    target = targets[randint(0, len(targets) - 1)]
                    swap(get_coord(data_1), target)
                elif cond_type == 'd':
                    targets = get_row_coords_neg(get_coord(data_1)[0])
                    if not targets:
                        counter = 1001
                        break
                    target = targets[randint(0, len(targets) - 1)]
                    swap(get_coord(data_1), target)
                elif cond_type == 'e':
                    targets = get_col_coords(get_coord(data_1)[1])
                    if not targets:
                        counter = 1001
                        break
                    target = targets[randint(0, len(targets) - 1)]
                    swap(get_coord(data_1), target)
                elif cond_type == 'f':
                    targets = get_col_coords_neg(get_coord(data_1)[1])
                    if not targets:
                        counter = 1001
                        break
                    target = targets[randint(0, len(targets) - 1)]
                    swap(get_coord(data_1), target)
    return counter <= 1000


def save(name):
    with open(name, 'w') as f:
        f.write(json.dumps({'layout': layout_format, 'conds': conds}, indent=2))


def load(name):
    global layout_format
    global conds
    with open(name) as f:
        data = json.load(f)
    layout_format = data.get('layout')
    conds = data.get('conds')


def prep_layout():
    global layout
    global layout_format
    layout = []
    for row_format in layout_format:
        row = []
        for seat_format in row_format:
            row.append(0 if seat_format == '0' else None)
        layout.append(row)


def gen():
    global layout
    global table
    b = True
    counter = 0
    while b and counter <= 1000:
        b = False
        counter += 1
        prep_layout()
        table = deepcopy(layout)
        nums = get_nums(count())
        for i in range(len(table)):
            for j in range(len(table[i])):
                if layout[i][j] == 0:
                    table[i][j] = get_num(nums)
        b = not valid_table()
    return counter <= 1000


def print_table():
    global layout_format
    global layout
    global table
    for i in range(len(layout)):
        output('', end='')
        for j in range(len(layout[i])):
            print('%5s'%(str(table[i][j]) if layout[i][j] == 0 else layout_format[i][j]), end='')
        print()


def print_layout():
    global layout_format
    if layout_format is None:
        output('layout not set')
        return
    for row in layout_format:
        output(' '.join([c for c in row]))


def set_layout(n):
    global layout_format
    layout_format = []
    for i in range(n):
        layout_format.append([c for c in get_input(f'row {i + 1}: ')])
    print()
    print_layout()


def print_conds():
    global conds
    if not conds:
        output('there are no conditions set yet')
        return
    output(f'there {"is" if len(conds) == 1 else "are"} {len(conds)} condition{"" if len(conds) == 1 else "s"} set:')
    print()
    for i in range(len(conds)):
        cond = conds[i]
        output(f'condition #{i + 1} (type: {cond.get("type")}, data_1: {cond.get("data_1")}, data_2: {cond.get("data_2")})')


print()
print('Seating Table Arrangment Program (STAP) v3.0')
while True:
    print()
    command = input('$ ')
    args = command.split(' ')
    print()
    try:
        if len(args) == 0 or args[0] == 'help':
            output_command('layout', 'display layout')
            output_command('layout set <rows>', 'set layout')
            output_command('cond', 'display conditions')
            output_command('cond add <type> <data_1> <data_2>', 'add condition')
            output_command('cond remove <index>', 'remove condition')
            output_command('cond remove all', 'remove all conditions')
            output_command('gen', 'generate a seating table')
            output_command('save <name>', 'save layout and conditions')
            output_command('load <name>', 'load layout and conditions')
            output_command('exit', 'exit the application')
            continue
        elif args[0] == 'layout':
            if len(args) == 1:
                print_layout()
                continue
            elif len(args) == 3 and args[1] == 'set':
                set_layout(int(args[2]))
                continue
        elif args[0] == 'cond':
            if len(args) == 1:
                print_conds()
                continue
            elif args[1] == 'add' and len(args) == 5:
                conds.append({'type': args[2], 'data_1': int(args[3]), 'data_2': int(args[4])})
                output(f'added a condition as condition #{len(conds)} (type: {args[2]}, data_1: {args[3]}, data_2: {args[4]})')
                continue
            elif args[1] == 'remove' and len(args) == 3:
                if args[2] == 'all':
                    conds.clear()
                    output('removed all conditions')
                else:
                    cond = conds[int(args[2]) - 1];
                    del conds[int(args[2]) - 1]
                    output(f'removed condition #{args[2]} (type: {cond.get("type")}, data_1: {cond.get("data_1")}, data_2: {cond.get("data_2")})')
                continue
        elif args[0] == 'gen' and len(args) == 1:
            if gen():
                print_table()
            else:
                output('timed out')
            continue
        elif args[0] == 'save' and len(args) == 2:
            save(args[1])
            output(f'saved to file "{args[1]}"')
            continue
        elif args[0] == 'load' and len(args) == 2:
            load(args[1])
            output(f'loaded from file "{args[1]}"')
            continue
        elif args[0] == 'exit':
            break
        output('invalid command usage')
    except:
        output('something unexpected occured')
