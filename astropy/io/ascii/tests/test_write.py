# Licensed under a 3-clause BSD style license - see LICENSE.rst
import sys

try:
    import StringIO as io
except ImportError:
    import io

from ... import ascii as asciitable

from .common import (raises,
                     assert_equal, assert_almost_equal, assert_true,
                     setup_function, teardown_function)

test_defs = [
    dict(kwargs=dict(),
         out="""\
ID XCENTER YCENTER MAG MERR MSKY NITER SHARPNESS CHI PIER PERROR
14 138.538 256.405 15.461 0.003 34.85955 4 -0.032 0.802 0 No_error
18 18.114 280.170 22.329 0.206 30.12784 4 -2.544 1.104 0 No_error
"""
         ),
    dict(kwargs=dict(delimiter=None),
         out="""\
ID XCENTER YCENTER MAG MERR MSKY NITER SHARPNESS CHI PIER PERROR
14 138.538 256.405 15.461 0.003 34.85955 4 -0.032 0.802 0 No_error
18 18.114 280.170 22.329 0.206 30.12784 4 -2.544 1.104 0 No_error
"""
         ),
    dict(kwargs=dict(formats={'XCENTER': '%12.1f',
                              'YCENTER': '{0:.1f}'},
                     include_names=['XCENTER', 'YCENTER'],
                     strip_whitespace=False),
         out="""\
XCENTER YCENTER
"       138.5" 256.4
"        18.1" 280.2
"""
         ),   
    dict(kwargs=dict(Writer=asciitable.Rdb, exclude_names=['CHI']),
         out="""\
ID	XCENTER	YCENTER	MAG	MERR	MSKY	NITER	SHARPNESS	PIER	PERROR
N	N	N	N	N	N	N	N	N	S
14	138.538	256.405	15.461	0.003	34.85955	4	-0.032	0	No_error
18	18.114	280.170	22.329	0.206	30.12784	4	-2.544	0	No_error
"""
         ),   
    dict(kwargs=dict(Writer=asciitable.Tab),
         out="""\
ID	XCENTER	YCENTER	MAG	MERR	MSKY	NITER	SHARPNESS	CHI	PIER	PERROR
14	138.538	256.405	15.461	0.003	34.85955	4	-0.032	0.802	0	No_error
18	18.114	280.170	22.329	0.206	30.12784	4	-2.544	1.104	0	No_error
"""
         ),   
    dict(kwargs=dict(Writer=asciitable.NoHeader),
         out="""\
14 138.538 256.405 15.461 0.003 34.85955 4 -0.032 0.802 0 No_error
18 18.114 280.170 22.329 0.206 30.12784 4 -2.544 1.104 0 No_error
"""
         ),   
    dict(kwargs=dict(Writer=asciitable.CommentedHeader),
         out="""\
# ID XCENTER YCENTER MAG MERR MSKY NITER SHARPNESS CHI PIER PERROR
14 138.538 256.405 15.461 0.003 34.85955 4 -0.032 0.802 0 No_error
18 18.114 280.170 22.329 0.206 30.12784 4 -2.544 1.104 0 No_error
"""
         ),   
    dict(kwargs=dict(Writer=asciitable.Latex),
         out="""\
\\begin{table}
\\begin{tabular}{ccccccccccc}
ID & XCENTER & YCENTER & MAG & MERR & MSKY & NITER & SHARPNESS & CHI & PIER & PERROR \\\\
14 & 138.538 & 256.405 & 15.461 & 0.003 & 34.85955 & 4 & -0.032 & 0.802 & 0 & No_error \\\\
18 & 18.114 & 280.170 & 22.329 & 0.206 & 30.12784 & 4 & -2.544 & 1.104 & 0 & No_error \\\\
\\end{tabular}
\\end{table}
"""
         ),
    dict(kwargs=dict(Writer=asciitable.AASTex),
         out="""\
\\begin{deluxetable}{ccccccccccc}
\\tablehead{\\colhead{ID} & \\colhead{XCENTER} & \\colhead{YCENTER} & \\colhead{MAG} & \\colhead{MERR} & \\colhead{MSKY} & \\colhead{NITER} & \\colhead{SHARPNESS} & \\colhead{CHI} & \\colhead{PIER} & \\colhead{PERROR}}
\\startdata
14 & 138.538 & 256.405 & 15.461 & 0.003 & 34.85955 & 4 & -0.032 & 0.802 & 0 & No_error \\\\
18 & 18.114 & 280.170 & 22.329 & 0.206 & 30.12784 & 4 & -2.544 & 1.104 & 0 & No_error \\\\
\\enddata
\\end{deluxetable}
"""
         ),
    dict(kwargs=dict(Writer=asciitable.AASTex, caption = 'Mag values \\label{tab1}', latexdict = {'units':{'MAG': '[mag]', 'XCENTER': '[pixel]'}}),
         out="""\
\\begin{deluxetable}{ccccccccccc}
\\tablecaption{Mag values \\label{tab1}}
\\tablehead{\\colhead{ID} & \\colhead{XCENTER} & \\colhead{YCENTER} & \\colhead{MAG} & \\colhead{MERR} & \\colhead{MSKY} & \\colhead{NITER} & \\colhead{SHARPNESS} & \\colhead{CHI} & \\colhead{PIER} & \\colhead{PERROR}\\\\ \\colhead{ } & \\colhead{[pixel]} & \\colhead{ } & \\colhead{[mag]} & \\colhead{ } & \\colhead{ } & \\colhead{ } & \\colhead{ } & \\colhead{ } & \\colhead{ } & \\colhead{ }}
\\startdata
14 & 138.538 & 256.405 & 15.461 & 0.003 & 34.85955 & 4 & -0.032 & 0.802 & 0 & No_error \\\\
18 & 18.114 & 280.170 & 22.329 & 0.206 & 30.12784 & 4 & -2.544 & 1.104 & 0 & No_error \\\\
\\enddata
\\end{deluxetable}
"""
         ),
    dict(kwargs=dict(Writer=asciitable.Latex, caption = 'Mag values \\label{tab1}', latexdict = {'preamble':'\\begin{center}', 'tablefoot':'\\end{center}', 'data_end':['\\hline','\\hline'], 'units':{'MAG': '[mag]', 'XCENTER': '[pixel]'}}, col_align='|lcccccccccc|'),
         out="""\
\\begin{table}
\\begin{center}
\\caption{Mag values \\label{tab1}}
\\begin{tabular}{|lcccccccccc|}
ID & XCENTER & YCENTER & MAG & MERR & MSKY & NITER & SHARPNESS & CHI & PIER & PERROR \\\\
 & [pixel] &  & [mag] &  &  &  &  &  &  &  \\\\
14 & 138.538 & 256.405 & 15.461 & 0.003 & 34.85955 & 4 & -0.032 & 0.802 & 0 & No_error \\\\
18 & 18.114 & 280.170 & 22.329 & 0.206 & 30.12784 & 4 & -2.544 & 1.104 & 0 & No_error \\\\
\\hline
\\hline
\\end{tabular}
\\end{center}
\\end{table}
"""
         ),
    dict(kwargs=dict(Writer=asciitable.Latex, latexdict = asciitable.latexdicts['template']),
         out="""\
\\begin{tabletype}
preamble
\\caption{caption}
\\begin{tabular}{col_align}
header_start
ID & XCENTER & YCENTER & MAG & MERR & MSKY & NITER & SHARPNESS & CHI & PIER & PERROR \\\\
 &  &  &  &  &  &  &  &  &  &  \\\\
header_end
data_start
14 & 138.538 & 256.405 & 15.461 & 0.003 & 34.85955 & 4 & -0.032 & 0.802 & 0 & No_error \\\\
18 & 18.114 & 280.170 & 22.329 & 0.206 & 30.12784 & 4 & -2.544 & 1.104 & 0 & No_error \\\\
data_end
\\end{tabular}
tablefoot
\\end{tabletype}
"""
         ),

]

tab_to_fill = ['a b c','1 2 3','1 1 3']

test_defs_fill_value = [
    dict(kwargs=dict(),
         out="""\
a b c
1 2 3
1 1 3
"""
         ),   
    dict(kwargs=dict(fill_values = ('1','w')),
         out="""\
a b c
w 2 3
w w 3
"""
         ),   
    dict(kwargs=dict(fill_values = ('1','w', 'b')),
         out="""\
a b c
1 2 3
1 w 3
"""
         ), 
    dict(kwargs=dict(fill_values = ('1','w'),
                     fill_include_names = ['b']),
         out="""\
a b c
1 2 3
1 w 3
"""
         ), 
    dict(kwargs=dict(fill_values = ('1','w'),
                     fill_exclude_names = ['a']),
         out="""\
a b c
1 2 3
1 w 3
"""
         ),
    dict(kwargs=dict(fill_values = ('1','w'),
                     fill_include_names = ['a'],
                     fill_exclude_names = ['a', 'b']),
         out="""\
a b c
1 2 3
1 1 3
"""
         ),
    dict(kwargs=dict(fill_values = [('1','w')],
                     formats={'a': '%4.2f'}),
         out="""\
a b c
1.00 2 3
1.00 w 3
"""
         ),
]


def check_write_table(test_def, table):
    out = io.StringIO()
    asciitable.write(table, out, **test_def['kwargs'])
    print('Expected:\n%s' % test_def['out'])
    print('Actual:\n%s' % out.getvalue())
    assert out.getvalue().splitlines() == test_def['out'].splitlines()


def test_write_table():
    table = asciitable.get_reader(Reader=asciitable.Daophot)
    data = table.read('t/daophot.dat')

    for test_def in test_defs:
        check_write_table(test_def, data)


def test_write_fill_values():
    data = asciitable.read(tab_to_fill)

    for test_def in test_defs_fill_value:
        check_write_table(test_def, data)

