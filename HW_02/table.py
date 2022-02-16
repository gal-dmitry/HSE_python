### easy


def generate_table(data):
    
    start = '\\documentclass{article}\n\\begin{document}\n\\begin{center}\n'
    end = '\\end{center}\n\\end{document}'
    tbl = '\\begin{tabular}{' + f'{" c " * len(data[0])}' + '}\n' +\
           '\n\\\\\n'.join(map(lambda x: ' & '.join(x), data)) + '\n\\end{tabular}\n'
    
    return start + tbl + end



if __name__ == '__main__':
    
    data = [['example', 'example', 'example'],
            ['example', 'example', 'example'],
            ['example', 'example', 'example']]
    
    with open('artefacts/table.tex', 'w') as f:
        f.write(generate_table(data))