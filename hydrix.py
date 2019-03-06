# -*- coding: utf-8 -*-
# AUTHOR : https://github.com/asciimist
from common import *
from CustomOrderedDict import *
from os import getcwd, environ, stat, sep, listdir
from os.path import expanduser, isdir, isfile, dirname, basename
from sys import exit, argv
from re import sub, match, search, finditer, compile
from re import split as re_split
from time import localtime, strftime
from datetime import timedelta
from math import log

global HOME
HOME = expanduser("~")

global SUSPENSION
SUSPENSION = 0

global hy_cscope
hy_cscope = int(environ["HY_CSCOPE"])

global argv_col
if hy_cscope :
    argv_col = '85,124,252'
else:
    argv_col = argv[3]

global arrow_col
arrow_col = "34"

global dicu
if int(environ["HY_UNICODE"])==1 :
    dicu = {
    'time' : u"🕛" ,
    'anchor' : u'⚓',
    'anchor-void' : u' ⚓∅ ',
    'flag' : u'📜',
    'find' : u'🔎',
    }
else :
    dicu = {
    'time' : u"[time-span]=" ,
    'anchor' : u'[path-root]=',
    'anchor-void' : u' [path-root]=None ',
    'flag' : u'[session-name]=',
    'find' : u'[path-filter]=',
    }

global H, I, L, F, T

H = u"─"
I = u"│"
F = u'├'

if environ["HY_REVERSE"]=="0" :
    L = u"└"
    T = u'┬'
else :
    L = u"┌"
    T = u'┴'

def _repr_timedelta(tdelta, bound99=1) :
    tdelta_seconds, tdelta_mins, tdelta_hours, tdelta_days = _print_timedelta(tdelta, bound99=0)
    res = ''
    if   tdelta_days>0    : res += "%ij" %(tdelta_days)
    elif tdelta_hours>0   : res += "%ih" %(tdelta_hours)
    elif tdelta_mins>0    : res += "%im" %(tdelta_mins)
    elif tdelta_seconds>0 : res += "%is" %(tdelta_seconds)
    return res

def rainbow(this_time, tdelta, min_time, max_time) :
    this_time = eval(this_time.replace('s', '').replace('m', '*60').replace('h', '*3600').replace('j', '*3600*24'))
    min_time = eval(_repr_timedelta(min_time, bound99=0).replace('s', '').replace('m', '*60').replace('h', '*3600').replace('j', '*3600*24'))
    max_time = eval(_repr_timedelta(max_time, bound99=0).replace('s', '').replace('m', '*60').replace('h', '*3600').replace('j', '*3600*24'))
    colors = [
    [ 255,  0 ,   0],
    [ 255, 127,   0],
    [ 255, 255,   0],
    [   0, 128,   0],
    [   0,   0, 255],
    [  75,   0, 130],
    [ 255,  51, 153],
    [   0,  0 ,   0],
    ]
    len_colors = len(colors)
    ttime = this_time
    color1 = max(0, min(int((ttime-min_time)*(len_colors-2)/(max_time-min_time)), len_colors-1))
    remainder_color1 = max(0.0, float(ttime-min_time)*(len_colors-2)/float(max_time-min_time)-float(color1))
    color2 = max(0, min(color1 + 1, len_colors-1))
    ini_color = colors[color1]
    fin_color = colors[color2]
    ret_color = [ e + int((fin_color[ie]-e)*(remainder_color1)) for ie,e in enumerate(ini_color) ]
    return ret_color


def color_time(this_time, tdelta, min_time, max_time) :
    ini_color = [ 255, 51, 153 ]
    ini_color = [ 256, 256, 10 ]
    fin_color = [ 0, 0, 0 ]
    _this_time = tdelta
    _min_time = eval(_repr_timedelta(min_time, bound99=0).replace('s', '').replace('m', '*60').replace('h', '*3600').replace('j', '*3600*24'))
    _max_time = eval(_repr_timedelta(max_time, bound99=0).replace('s', '').replace('m', '*60').replace('h', '*3600').replace('j', '*3600*24'))
    if _min_time==_max_time :
        return "\033[38;2;"+(';'.join([str(ini_color[0]), str(ini_color[1]), str(ini_color[2])]))+"m"
    elif _this_time==_min_time :
        return "\033[38;2;"+(';'.join([str(ini_color[0]), str(ini_color[1]), str(ini_color[2])]))+"m"
    try :
        ret_color = rainbow(this_time, tdelta, min_time, max_time)
    except ZeroDivisionError :
        ret_color = ini_color
    return "\033[38;2;"+(';'.join([str(e) for e in ret_color]))+"m"


def _print_timedelta(tdelta, bound99=1) :
    tdelta_seconds = tdelta
    if bound99 :
        tdelta_days = min(tdelta_seconds/(24*3600), 99)
    else :
        tdelta_days = tdelta_seconds/(24*3600)
    tdelta_hours = tdelta_seconds/3600
    tdelta_mins = (tdelta_seconds%3600)/60
    tdelta_seconds = (tdelta_seconds%3600)%60
    return tdelta_seconds, tdelta_mins, tdelta_hours, tdelta_days


def repr_timedelta(tdelta, tmin=None, tmax=None) :
    res = _repr_timedelta(tdelta)
    if tmin and tmax :
        return color_time(res, tdelta, tmin, tmax)+('%3s'%res)
    else :
        return res

def print_collapsed(nb_collapsed) :
    collapsed_mark_start, collapsed_mark_stop = '', ''
    if nb_collapsed>0 :
        collapsed_mark_start = u'\033[7m'
        collapsed_mark_stop = '+'+str(nb_collapsed)+u'\033[7m'
    return collapsed_mark_start, collapsed_mark_stop

def print_timedelta(tdelta1, tdelta2, count_hist_p, NOTE, nb_collapsed) :
    res = repr_timedelta(tdelta1)
    if res== '' : res = '0'
    res += '~'
    res += repr_timedelta(tdelta2)
    if res=='0~' : res = '0~0'
    end = u" "
    collapsed_mark_start, collapsed_mark_stop = print_collapsed(nb_collapsed)
    return collapsed_mark_start+'('+res + ')(%i!) %s'%(count_hist_p, NOTE)+ collapsed_mark_stop

def eagle(i_tty, N_LAST_PLACES, N_MIN_CMDS_AT_PLACE_FOR_DISPLAY, COLUMNS, root, nb_h_lines, hgrep, highlight_col, hy_cd, filter_time=None) :
    if verb==2 : print "@eagle"
    numbers = [ u'[%i] '%i for i in range(1,10) ] + [ u'[%i]'%i for i in range(10,100) ]
    highlander = environ["HY_GHLANDER"]
    if not filter_time and environ["HY_TIME_FILTER"] :
       filter_time = environ["HY_TIME_FILTER"]
    if hgrep : print "hgrep", repr(hgrep),
    elif environ["HY_GREP"] :
        hgrep = environ["HY_GREP"]
    op = open(HOME+"/.hydrix/history/pwd.%i"%i_tty)
    oppp = open(HOME+"/.hydrix/history/pwd_filtered.%i"%i_tty, "w")
    hname = ""
    rd = op.readlines()
    op.close()
    rd_ini = rd[:]
    if rd and rd[0][0]=='#' :
        hname = rd[0][1:].strip()
        rd = rd[1:]
    if rd and rd[0][0]=='#' :
        print "[NAME] more than 1 comment/name line in "+  HOME+"/.hydrix/history/pwd.%i"%i_tty
        print "\033[0;00m"
        exit()
    if not hy_cscope :
        rd = list(reversed(rd))
    if rd==[] :
        print "[EMPTY] "+  HOME+"/.hydrix/history/pwd.%i"%i_tty
        print "\033[0;00m"
        exit()
    places =[]
    root = root.rstrip()
    root = root.decode('utf8', 'replace')
    if root=='.' :
        if not hy_cscope :
            if verb==2 : print "\033[0;37m'%s' -> '%s'"%(root, getcwd())
            root = getcwd()
        else :
            root = hy_cd
        #_root = u' ⚓. '
        _root = dicu['anchor']+u' . '
    elif root=='pwd' :
        if not hy_cscope :
            root = getcwd()
        else :
            root = hy_cd
        op = open(HOME+"/.hydrix/history/root.%i"%i_tty, "w")
        op.write("%s\n"%root)
        op.close()
        _root = u' '+dicu['anchor']+root[:]+' '
    else :
        _root = root[:]
        if not root : _root = dicu['anchor-void']
    if _root!=dicu['anchor-void'] : _root = u'\033[7m'+_root+u'\033[0;37m'
    print_root =  u"\033[0;37m %s %s \033[3m\"%s\""%(_root, dicu['flag'], hname.decode('utf8', 
'replace'))
    if hgrep : print_root +=  u"%s %s "%(dicu['find'], hgrep.decode('utf8', 'replace'))
    print print_root,
        #print " %s 
    root = root.encode('utf8', 'replace')
    _local_time = int(strftime("%s", localtime()))
    prev_place = ''
    prev_hist_time = -1
    cmds = []
    #ignored_commands = ("slw", "cd", "ls", "ll" , "lha" , "pp" , "h", "l", "top", "more", "kate", "bg", "fg", "kelg", 'sudo mount', 'sudo umount') # ignored 
    opc = open(HOME+"/.hydrix/IGNORED_COMMANDS")
    ignored_commands = [ _.replace("*", ".*") for _ in opc.readlines() ]
    opc.close()
    opc = open(HOME+"/.hydrix/IGNORED_PATHS")
    ignored_paths = [ _.strip().replace("*", ".*") for _ in opc.readlines() ]
    opc.close()
    one_match = None
    if filter_time :
        print dicu['time'], filter_time
        print_root +=  dicu['time']+" %s "%(filter_time.decode('utf8', 'replace'))
        filter_time_min, filter_time_max = [ e for e in 
filter_time.replace('m', 
'*60').replace('h', '*3600').replace('j', '*3600*24').split('~')]
        if filter_time_max : filter_time_max = eval(filter_time_max)
        else               : filter_time_max = 10000000000
        if filter_time_min : filter_time_min = eval(filter_time_min)
        else               : filter_time_min = 0
    cmds_places = {}
    real_paths = {}
    times = {}
    sources = {}
    collapse = [ expanduser(_).decode('utf8') for _ in environ["HY_COLLAPSED"].split(":") ]
    collapsed = {}
    for i,elt in enumerate(rd) :
        spl = elt.split(" : ")
        place_orig = spl[1].decode('utf8', 'replace').replace('/local00/','/')
        if not place_orig.strip() : continue
        if hy_cscope :
            place_orig, source = place_orig.split(' @')
        if any([ match('^'+_+'\ ?.*$', place_orig) for _ in ignored_paths ]) : continue
        bbreak = 0
        for e in collapse :
            if e and e!=place_orig and e in place_orig :
                bbreak = 1
                if collapsed.has_key(e) :
                    collapsed[e].add(place_orig)
                else :
                    collapsed[e] = set([place_orig])
                break
        if bbreak==1 : continue
        place = place_orig.replace(' ','\0').replace('+','\1').replace('.','\2').replace('^','\3').replace('?','\4') 
        #replacing regex incompatible chars by chars impossible in a UNIX filename for latter substitution at equal string size
        if hy_cscope : 
            sources[place] = source
        spl_2 = spl[2]#.replace(u"�",'?')
        cmd = spl_2.decode('utf8', "replace")
        hist_time = 0
        if ( not any([ match('^'+_+'\ ?.*$', cmd) for _ in ignored_commands ]) or ';' in cmd ) and ( hgrep.strip()=='' or ( ('/' in hgrep and search(hgrep, place_orig)) or search(hgrep, cmd.strip()) ) ) and ( not root or expanduser(place_orig).startswith(expanduser(root.decode('utf8'))) ) :
            one_match = True
            real_paths[place] = place_orig[:]
            if environ["HY_ELLIPSIS"]=='1' and root and expanduser(place_orig).startswith(expanduser(root)) :
                _split = place[:len(root)].split('/')
                place = '/'+_split[0]+u'/'.join([ e[0]+u'…'+e[-1] for e in _split[1:-1]])+'/'+_split[-1]+place[len(root):]
                real_paths[place] = place_orig[:]
            if not hy_cscope:
                if isdir(expanduser(place_orig)) :
                    if stat(expanduser(place_orig))==stat(getcwd()) : path_is_current = True
                    else                                            : path_is_current = False
                else :
                    path_is_current = False
            else :
                path_is_current = False
                if place_orig==hy_cd :
                    path_is_current = True
            if '-' in spl[0] :
                hist_time = int(spl[0].split("-")[1])
                entry_timedelta = _local_time-hist_time
                if prev_place!=place :
                    if prev_hist_time==-1 :
                        boundary_timedelta = _local_time-hist_time
                    else :
                        boundary_timedelta = _local_time-prev_hist_time
                    if prev_place : times[prev_place].append(boundary_timedelta)
                    times[place] = [ boundary_timedelta ]
            else :
                times[place] = [ _local_time ] # to cure accidentally missing date in pwd.*
            prev_place = place
            prev_hist_time = hist_time
            if ( filter_time==None or ( filter_time_max>=entry_timedelta>=filter_time_min) ) and (not cmds_places.has_key(place) or cmd not in cmds_places[place]) :
                if not highlander or ( not cmds_places.has_key(place) or not cmds_places[place][-1].startswith(cmd.split(' ')[0]) ) :
                    places.append([place, path_is_current, hist_time])
                    if not cmds_places.has_key(place) :
                        cmds_places[place] = [cmd]
                    else :
                        cmds_places[place] += [cmd]
                    cmds.append(cmd)
    if prev_place :
        times[prev_place].append(_local_time-prev_hist_time)
        print ""
    else :
        if hgrep :
            print "[NOMATCH]"
            print "\033[0;00m"
            exit()
    for k,v in times.items() :
        if len(times[k])==1 : times[k].append(0)
    odict = CustomOrderedDict()
    visit_order = CustomOrderedDict()
    visit_order_last = CustomOrderedDict()
    max_mark = 0
    prev_p = None
    if not places :print "[EMPTY] places=[]" ; print "\033[0;00m" ; exit()
    for ip, (p, path_is_current, hist_time) in enumerate(places) :
        cmds_ip = [cmds[ip].strip() , '', 0]
        if not visit_order.has_key(p) : visit_order[p] = p
        visit_order_last[prev_p] = ip-1
        mark = visit_order.keys().index(p)
        max_mark = max(max_mark, mark)
        cmds_ip[2] = mark
        cmds_ip.append(hist_time)
        if mark > len(numbers)-1 : mark = "  "
        else                     : mark = numbers[mark]
        if path_is_current : cmds_ip[1] = (1, mark)
        else               : cmds_ip[1] = (0, mark)
        p2 = ''
        p_split = p.split('/')
        for e in p_split :
            if SUSPENSION and len(e)>COLUMNS/4 : e = e[:10]+u"…"+e[-10:]
            p2 += e+'/'
        p2 = p2[:-1]
        if not odict.has_key(p) :
            odict[p2] = [['', cmds_ip[1], cmds_ip[2]]]
        odict[p2].append( cmds_ip )
        prev_p = p
    visit_order_last[prev_p] = ip-1
    visit_order_last = [e[0]  for e in sorted(visit_order_last.items(), key=lambda t: t[1])]
    odict_items = odict.items()
    len_odict_items = len(odict_items)
    for k,v in odict_items :
        if hy_cscope : v = list(reversed(v))
        len_v = len(v)
        new = []
        times = []
        for ii in range(1, nb_h_lines) :
            if ii<=(len_v-1) :#and v[ii][-1]!=0 :
                times.append(_local_time -v[ii][-1])
        tmin = min(times)
        tmax = max(times)
        for i_hist in range(nb_h_lines) :
            i_hist_o = i_hist
            if i_hist<0 : break
            if i_hist_o<=(len_v-1) :
                v_i_hist = v[i_hist]
                marks = v_i_hist[1]
                _i_hist = i_hist
                hist_time = times[i_hist-1]
                if ( hy_cscope==0 and i_hist_o==0  ) or ( hy_cscope==1 and i_hist_o==(len_v-1) ) :
                    if marks[0]==0 : v_i_hist[1] = "\033[38;5;082m%s  \033[30m"%(marks[1],)
                    else           :
                        if not hy_cscope :
                            v_i_hist[1] = "\033[4;"+highlight_col+";37m%s  "%(marks[1])
                        else :
                            v_i_hist[1] = "\033[1;4;41;37m%s  "%(marks[1])
                else :
                    if ( hy_cscope==0 and i_hist_o==1 ) or ( hy_cscope==1 and i_hist_o==len_v-1-1 ) :
                        k_ = k.encode('utf8').replace('\0',' ').replace('\1','+').replace('\2','.').replace('\3','^').replace('\4','?')
                        if isfile(k_+"/NOTE") :
                            opa = open(k_+"/NOTE", 'r')
                            rda = opa.readlines()
                            opa.close()
                            NOTE = rda[0].decode('utf8')
                        elif isfile(k_+"/NOTE.lg") :
                            opa = open(k_+"/NOTE.lg", 'r')
                            rda = opa.readlines()
                            opa.close()
                            for l in rda :
                                l = l.decode('utf8')
                                if '#: ' in l :
                                    NOTE = NOTE[NOTE.index('#: '):]
                            else :
                                NOTE = 'name not found'
                        else :
                            NOTE= ''
                        nb_collapsed = ()
                        if k_.decode('utf8') in collapsed.keys() :
                            nb_collapsed = collapsed[k_.decode('utf8')]
                        nb_collapsed = len(nb_collapsed)
                        if not hy_cscope :
                            odict[k][0][0] = print_timedelta(tmin, tmax, len(cmds_places[k]), NOTE, nb_collapsed)
                        else :
                            collapsed_mark_start, collapsed_mark_stop = print_collapsed(nb_collapsed)
                            odict[k][0][0] = sources[k]+collapsed_mark_start+collapsed_mark_stop
                    oppp.write("%s : %s\n"%(k.encode('utf8'), v_i_hist[0].encode('utf8')))
                    if marks[0]==0 : v_i_hist[1] = "\033[30m%s:%s\033[37m "%(repr_timedelta(hist_time, tmin=tmin, tmax=tmax), i_hist_o)
                    else           : v_i_hist[1] = "\033["+highlight_col+";30m%s:%s\033[37m "%(repr_timedelta(hist_time, tmin=tmin, tmax=tmax), i_hist_o)
                new.append(v_i_hist)
            else :
                new.append([ "", 6*" ", 0 ])
        odict[k] = new[:]
    oppp.close()
    if  int(environ["HY_FREEZE"])==0 :
        opp = open(HOME+"/.hydrix/history/cwd.%i"%i_tty, 'w')
        for k in visit_order.keys() :
            opp.write("%s\n"%(real_paths[k].encode("utf8")) )
        opp.close()
    return odict, max_mark, print_root

def build_recursive_nest(head, flat, treated, nest, llist, level=0) :
    main_head = ""
    llist = [ e.rstrip(sep) for e in llist ]
    head = head.rstrip(sep)
    for p in flat :
        if match("^"+head+"/.*", p) :
            if level==0 :
                if len(main_head)<len(p)  : main_head = p
            flat.remove(p)
            treated.append(p)
            flat, treated, nest = build_recursive_nest(p, flat, treated, nest, llist, level=level+1)
    if main_head : head = main_head
    head_split = head.split('/')
    if head not in nest and head in llist : nest.append(head)
    if head in flat :
        flat.remove(head)
        treated.append(head)
    for ih in range(1, len(head_split)) :
        ih = -ih
        if ih==0 : ih = None
        h = "/".join(head_split[:ih])
        flat, treated, nest = build_recursive_nest(h, flat, treated, nest, llist, level=level-1)
    return flat, treated, nest

def line_to_colorLine(line) :
    if not isinstance(line, unicode) : line = line.decode('utf8', 'replace')
    reg = compile("(\\x1b\[[0-9;]*m)+")
    reg2 = compile("(([\[;]48;5;[0-9]{2,3}[;m])|([\[;]48;2;[0-9]{2,3};[0-9]{2,3};[0-9]{2,3}[;m])|([\[;]4[0-7][;m]))")
    iterator = reg.finditer(line)
    list_matches = list(iterator)
    spans = [ match.span() for match in list_matches ]
    prev_sp1, prev_sp2 = 0, 0
    llist = []
    prev_bg_color = '0'
    for (isp, (sp1, sp2)) in enumerate(spans) :
        if isp==0 :
            for e in line[:sp1] :
                llist.append([e, "\x1b[0m"])
        prev_bloc = line[prev_sp2:sp1]
        if isp > 0 :
            for ie,e in enumerate(prev_bloc) :
                llist.append([e, prev_color])
        cur_color = line[sp1:sp2]
        prev_sp1, prev_sp2 = sp1, sp2
        prev_color = cur_color
        for cc in cur_color.split('\x1b') :
            findall2 = reg2.findall(cc)
            if findall2 :
                prev_bg_color = findall2[0][0][1:-1]
    if spans==[] :
        sp2 = 0
        prev_color = "\x1b[0m"
    for e in line[sp2:]:
        llist.append([e, prev_color])
    return llist

def color_24bit_to_8bit(line) :
    reg = compile("(\\x1b\[[0-9;]*m)")
    reg2 = compile("(.*)([34]8;2;[0-9]{,3};[0-9]{,3};[0-9]{,3})(.*)")
    iterator = reg.finditer(line)
    list_matches = list(iterator)
    spans = [ match.span() for match in list_matches ]
    prev_sp1, prev_sp2 = 0, 0
    llist = []
    prev_bg_color = '0'
    res = ''
    for (isp, (sp1, sp2)) in enumerate(spans) :
        cur_color = line[sp1:sp2]
        between = line[prev_sp2:sp1]
        res += between
        prev_sp1, prev_sp2 = sp1, sp2
        tmp = []
        for cc in cur_color.split('\x1b') :
            m = reg2.match(cc)
            if m :
                findall2 = m.groups()
                _res = ''
                for e in findall2 :
                    if e.startswith('38;2;') or e.startswith('48;2;') :
                        r, g, b = e[5:].split(';')
                        _r, _g, _b = int(float(r)*5./255.), int(float(g)*5./255.), int(float(b)*5./255.)
                        color8 = 16 + 36 * _r + 6 * _g + _b
                        _res += "%s;5;%i"%(e[:2], color8)
                    else :
                        _res += e
                tmp.append(_res)
            else :
                tmp.append(cc)
        r= '\x1b'
        res += r.join(tmp)
    return res


def colorLine_to_line(llist) :
    res = ""
    prev_color = ""
    for e,c in llist :
        if c!=prev_color :
            res += c
        res += e
        prev_color = c
    return res

def norm(spacer, sstr, force=1, filling_char=u' ', shift=0) :
    if spacer<0 : return ''
    line_to_colorLine_sstr = line_to_colorLine(sstr)
    len_sstr = len(line_to_colorLine_sstr)
    start_char, end_char = u"…", u"…"
    if   shift==0  :
        start_char = u""
        starter = 0
        ender   = spacer-1
    elif shift>0 or shift<0:
        starter = shift*spacer+1
        ender   = (shift+1)*spacer-1
    elif shift==-1 :
        end_char = u""
        starter = shift*spacer+1
        ender   = len_sstr
    if not spacer : return sstr
    else:
        if filling_char!=u' ' :print "'\x1b' not in sstr ", '\x1b' not in sstr
        if '\x1b' not in sstr :
            res = ("%-"+str(spacer)+"s")%sstr
            if len(res)>spacer :
                return start_char+res[starter:ender]+end_char
            return res
        else :
            char_list, color_list = zip(*line_to_colorLine_sstr)
            char_list, color_list = list(char_list), list(color_list)
            if len_sstr>spacer :
                c = []
                if shift!=0  : c += [ color_list[starter] ]
                c += color_list[starter:min(ender, len_sstr)]
                if shift!=-1 : c += [ color_list[min(ender, len_sstr)] ]
                s = start_char+(''.join(char_list[starter:ender]))+end_char
                res = colorLine_to_line(zip(s, c))
            else :
                if force :
                    c = color_list[:min(spacer, len_sstr)-1] + [ color_list[-1] for d in range(spacer-len_sstr+1) ]
                    s = ''.join(char_list)+(filling_char*(spacer-len_sstr+1))
                    if filling_char!=u' ': print "s", s
                    res = colorLine_to_line(zip(s, c))+'\033[0m'
                else :
                    res = sstr
            return res

def _color_tty(i_mark, max_mark, __argv__) :
    highlight_col = "48;2;"+argv_col.replace(',',';')+";094"
    if max_mark==0 : return highlight_col
    fin_color = [ int(e) for e in argv_col.split(',') ]
    ini_color = [int(e) for e in highlight_col.split(';')[2:]]
    ini_color = [ int(e) for e in argv_col.split(',') ]
    fin_color = [ 64 , 64, 64 ]
    ret_color = [ e + int((fin_color[ie]-e)*float(i_mark)/float(max_mark)) for ie,e in enumerate(ini_color) ]
    return "48;2;"+(';'.join([str(e) for e in ret_color]))+";094"

def unspace_path(path) :
    return sub('(?<!\\\) ', '' ,path)

def split_blocks(sorted_nest_groups, odict, __argv__, spacer, shortened_path_dict, max_mark, COLUMNS, nb_h_lines, highlight_col, original_path_dict, print_root) :
    splitted_head_list = [ ]
    for ig, gr in enumerate(sorted_nest_groups[:]) :
        head_gr = gr
        head_full = head_gr[0][0].rstrip()
        head = shortened_path_dict[head_full]
        separator_positions = [ (len(e[0]), e[1]) for e in head_gr[1:] ]
        separator_positions.sort(key=lambda x:x[0])
        splitted_head = [ ]
        isep_prev = 0
        for isep, hist_entry in separator_positions :
            splitted_head.append( (head[isep_prev:isep], hist_entry) )
            isep_prev = isep
        splitted_head.append( (head[isep_prev:], odict[sub('(?<!\\\) ', '' ,head_full)]) )
        splitted_head_list.append(splitted_head)
    prev_spl = None
    longest_rest_list = []
    res = []
    arrow_pos = [ -1 for dum in range(len(splitted_head_list)+1) ]
    SQUARE = environ["HY_TRUE_COLORS"]
    focus = environ["HY_FOCUS"].decode('utf8', 'replace')
    if focus==u'' : focus = u'-1'
    def color_tty(i_mark, max_mark) : return _color_tty(i_mark, max_mark, __argv__)
    to_be_highlighted, i_to_be_highlighted = "NeVeR", 0
    colors_found = []
    for isp, tuple_spl_and_hist in enumerate(splitted_head_list) :
        spl = [ e[0] for e in tuple_spl_and_hist ]
        if isp==0 :
            tmp_res = []
            for i_hist in range(nb_h_lines) :
                hist_line = []
                for ie,e in enumerate(tuple_spl_and_hist) :
                    e1 = e[1]
                    if len(e1)-1>=i_hist :
                        piece_hist_line = e1[i_hist]
                        hist_line.append(piece_hist_line)
                    else :
                        hist_line.append([ "", prev_hist_line[ie][1], 0 ])
                prev_hist_line = hist_line[:]
                if i_hist==0 : hist_line_ = hist_line[:]
                tt = ''
                if hist_line[0][1]!= 6*" " or SQUARE :
                    color_entry_0 = color_tty(hist_line[0][2], max_mark)
                    tt += ('\033[0;'+color_entry_0+';37m')
                path_pieces = [ spl[0].rstrip(sep) ] + [ e.strip(sep) for e in spl[1:] ]
                for ie,e in enumerate(hist_line) :
                    spaced_full_path = '/'.join(path_pieces[:ie+1]).rstrip()
                    unspaced_full_path = unspace_path(spaced_full_path)
                    #if hist_line[ie][1]!= 6*" " or SQUARE :
                    if 1 :
                        color_entry = color_tty(hist_line_[ie][2], max_mark)
                        tt += ('\033[0m\033[0;'+color_entry+';37m')
                    if i_hist==0 : colors_found.append(color_entry)
                    sstr = hist_line[ie][1]+e[0]
                    if focus!=u'-1' :
                        if unspaced_full_path==focus : len_to_format_ie = COLUMNS - 10
                        else         : len_to_format_ie = 2
                    else : 
                        len_to_format_ie = len(path_pieces[ie])
                        len_to_format_ie = max(len(path_pieces[ie]), spacer)
                    if focus==u'-1' or (focus!=u'-1' and unspaced_full_path==focus) :
                        if sstr!=6*' '  :
                            tt += norm(len_to_format_ie, sstr)+ '\033[0m '
                        else            : tt += '\033[0m '+(len_to_format_ie*' ')
                    elif focus!=u'-1' and unspaced_full_path!=focus :
                        tt += '\033[0m '
                tmp_res.append( tt )
            tmp_res = list(reversed(tmp_res))
            res += tmp_res[:]
            ll = u''
            for ie,l in enumerate(path_pieces) :
                spaced_full_path = '/'.join(path_pieces[:ie+1]).rstrip()
                unspaced_full_path = original_path_dict[spaced_full_path]
                unspaced_full_path = unspace_path(spaced_full_path)
                color_highlight =  match("^(\\x1b\[[0-9;]*m)", hist_line_[ie][1]).groups()[0]
                if highlight_col in color_highlight : to_be_highlighted, i_to_be_highlighted = l, 0
                if focus!=u'-1' :
                    if unspaced_full_path==focus : ll += norm(COLUMNS - 10, l)
                else :
                    len_to_format_ie = max(len(path_pieces[ie]), spacer)
                    ll += norm(len_to_format_ie, l)
                ll += H
            ll = ll[:-1]
            res.append( ll )
            res.append( " "*(COLUMNS*4) )
            if focus!=u'-1' : break
        else :
            spl_0_split = spl[0].split(sep)
            prev_spl_ = prev_spl[:]
            prev_spl = sep.join(prev_spl)
            prev_spl_0_split = [u'']+[ e for ie, e in enumerate(prev_spl.split(sep)) if e ]
            len_spl_0_split, len_prev_spl_0_split = len(spl_0_split), len(prev_spl_0_split)
            for i_s in range(max(len_spl_0_split, len_prev_spl_0_split)) :
                if i_s>len_spl_0_split-1 or i_s>len_prev_spl_0_split-1 or spl_0_split[i_s]!=prev_spl_0_split[i_s] : break
            longest_common , longest_rest = spl_0_split[:i_s], spl_0_split[i_s:]
            spl_0_longest_rest = ('/'.join(longest_rest))
            spl_0_longest_common = ('/'.join(longest_common))
            rest = [ e.strip(sep) for e in spl[1:] ]
            len_spl_0_longest_common = len(spl_0_longest_common)
            arrow_pos[isp] = len_spl_0_longest_common
            pad = u" "
            if len_spl_0_longest_common==0 : pad = u""
            path_pieces = [ spl_0_longest_rest.strip(sep) ]+rest
            ##########################################################################"
            tmp_res = []
            for i_hist in range(nb_h_lines) :
                hist_line = []
                for ie,e in enumerate(tuple_spl_and_hist) :
                    if len(e[1])-1>=i_hist :
                        hist_line.append(e[1][i_hist])
                    else :
                        hist_line.append([ "", prev_hist_line[ie][1], 0 ])
                prev_hist_line = hist_line[:]
                tt = ''
                tt += (u" "*(len_spl_0_longest_common+1))
                if i_hist==0 : hist_line_ = hist_line[:]
                #if hist_line[0][1]!=6*" "  or SQUARE :
                if 1 :
                    color_entry_0 = color_tty(hist_line[0][2], max_mark)
                    tt+=(u'\033[0;'+color_tty(hist_line[0][2], max_mark)+';37m')
                for ie,e in enumerate(hist_line) :
                    if hist_line[ie][1]!= 6*" " or SQUARE :
                        color_entry = color_tty(hist_line[ie][2], max_mark)
                        tt += ('\033[0m\033[0;'+color_entry+';37m')
                    if i_hist==0 :
                        colors_found.append(color_entry)
                    sstr = hist_line[ie][1]+e[0]
                    len_to_format_ie = max(len(path_pieces[ie]), spacer)
                    if sstr!=6*' ' : tt += norm(len_to_format_ie, sstr)+ '\033[0m '
                    else           : tt += '\033[0m '+len_to_format_ie*' '
                tmp_res.append( tt )
            tmp_res = list(reversed(tmp_res))
            res += tmp_res[:]
            ##########################################################################"
            ll = pad+(u" "*(len_spl_0_longest_common-1))+L#+H.join(path_pieces)
            for ie,l in enumerate(path_pieces) :
                spaced_full_path = '/'.join(path_pieces[:ie+1]).rstrip()
                unspaced_full_path = unspace_path(spaced_full_path)
                color_highlight = match("^(\\x1b\[[0-9;]*m)", hist_line_[ie][1]).groups()[0]
                if highlight_col in color_highlight : to_be_highlighted, i_to_be_highlighted = l, 0
                if focus!=u'-1' :
                    if unspaced_full_path==focus : ll += norm(COLUMNS - 10, l)
                else :
                    len_to_format_ie = max(len(path_pieces[ie]), spacer)
                    ll += norm(len_to_format_ie, l)
                ll += H
            ll = ll[:-1]
            res.append( ll )
            res.append(" "*(COLUMNS*4) )
        prev_spl = spl
    max_len_res = max([ len(line_to_colorLine(l)) for l in res if l!=' '*len(l)])
    for i in range(len(res)) :
        l = res[i]
        actual_str_len = len(line_to_colorLine(l))
        if l!=' '*len(l) :
            res[i] = res[i]+'\033[0m'+(' '*(max_len_res-actual_str_len))
        else :
            res[i] = (' '*(max_len_res))
    for i in range(len(res)-1, 0, -1) :
        """Completing the tracing of arrows"""
        j = i-1
        arrow_pos_i = arrow_pos[(i+1)/(nb_h_lines+2)] #(i+1) for last empty line ; (nb_h_lines+2) for path line and the blank spacing line
        res_j = res[j]
        while j>nb_h_lines and res[j][arrow_pos_i]==u" " and arrow_pos_i!=-1 :
            line = list(res[j])
            line[arrow_pos_i] = I
            res[j] = ''.join(line)
            j -= 1
        line = list(res[j])
        if line[arrow_pos_i]==H : line[arrow_pos_i] = T
        if line[arrow_pos_i]==L : line[arrow_pos_i] = F
        res[j] = ''.join(line)
    _res = []
    i_color = 0
    for il,l in enumerate(res) :
        """ Completing the coloring of cells"""
        l_new = ''
        for c in l :
            if il==nb_h_lines and i_color==0 and c=='/' :
                l_new += (u'\033[0;%s;37m/')%(colors_found[0])
                i_color = 1
            elif c in (F, T, L, H) :
                if il>nb_h_lines : _i_color = i_color +1
                else : _i_color = i_color
                _i_color = i_color
                l_new += (u'\033[0;1;'+arrow_col+'m%s\033[0;%s;37m')%(c, colors_found[_i_color])
                i_color += 1
            elif c==u'│':
                l_new += u'\033[1;'+arrow_col+'m%s\033[0;37m'%(c)
            else :
                l_new += c
        _res.append(l_new)
    res = _res[:]
    to_be_highlighted = to_be_highlighted.replace('*', '')
    res[i_to_be_highlighted+nb_h_lines] = sub('('+to_be_highlighted.replace('\ ', '\\\ ')+')', '\x1b[48;5;021m\g<1>', res[i_to_be_highlighted+nb_h_lines])
    count = 2 # (1:better to start value for modulo)+ (1 to compesante the missing first blank line)
    some_bash_cmds = ['awk', 'basename', 'cat', 'cd', 'cp', 'cut', 'echo', 'eval', 'exec', 'find', 'grep', 'head','kill', 'ls', 'less', 'ln', 'man', 'make', 'mkdir', 'more', 'mv', 'mount', 'python', 'printf', 'rm', 'rmdir','rsync', 'scp', 'sed', 'seq', 'ssh', 'sudo', 'sort' 'tail','touch', 'uniq', 'wc', ";", "\|"]
    for ie,e in enumerate(res) :
        ###### colorise '/' in black
        if ( count%(nb_h_lines+2)==0) : # (1 for the (nb_h_lines+path_line)) + (1 for the blank spacing line)
            comp = compile(ur"(\x1b\[[0-9;]*m|$)")
            fd_iter = list(finditer(comp, e))
            out = ""
            sp1_p = 0
            for im, m in enumerate(fd_iter) :
                sp0, sp1 = m.span()
                if sp1_p!=sp0 :
                    m1_split = e[sp1_p:sp0].split('/')
                    out += "/".join(m1_split[:-1] + [ '\033[38;5;255;1;3m'+m1_split[-1] ]) # bold and italics for basename
                out +=e[sp0:sp1]#+'\033[30m'
                sp1_p = sp1
            e = out
            e = e.replace("/", "\033[30m/\033[37m") # colorise '/' in black
            res[ie] = e
        elif ( count%(nb_h_lines+2)!=nb_h_lines+1) :
            bash_kw_col  = "111"
            block_kw_col = "129"
            string_col   = "106"
            option_col   = "220"
            vareval_col  = "172"
            path_col     = "142"
            subterm_col  = "154"
            for k in some_bash_cmds :
                e = sub("(\s)("+k+")([$\s])", "\g<1>\033[38;5;"+bash_kw_col+"m\g<2>\033[37m\g<3>", e)
            for k in 'for|in|if|else|then|do|done|fi'.split('|') :
                e = sub("([\s])("+k+")([$\s])", "\g<1>\033[38;5;"+block_kw_col+"m\g<2>\033[37m\g<3>", e)
            e = sub("([\s])(\"[^\"]*\")([$\s])", "\g<1>\033[38;5;"+string_col+"m\g<2>\033[37m\g<3>", e)
            e = sub("([\s])(\'[^\"]*\')([$\s])", "\g<1>\033[38;5;"+string_col+"m\g<2>\033[37m\g<3>", e)
            e = sub("([\s])(-[^\s]*)([$\s])", "\g<1>\033[38;5;"+option_col+"m\g<2>\033[37m\g<3>", e)
            e = sub("(\$\{[^\}]*\})", "\033[38;5;"+vareval_col+"m\g<1>\033[37m", e)
            e = sub("(\$?\()", "\033[38;5;"+subterm_col+"m\g<1>\033[37m", e)
            e = sub("(\))", "\033[38;5;"+subterm_col+"m\g<1>\033[37m", e)
            e = sub("(\))", "\033[38;5;"+subterm_col+"m\g<1>\033[37m", e)
            res[ie] = e
        count += 1
    res_ = []
    do_one = 1
    for il, l_ in enumerate(res) :
        """ suppressing blank hist lines to ouput more compact"""
        l_ = sub("\\x1b\[[0-9;]*m", '', l_.strip())
        if all( [ c==u' ' or c==u'\u2502' for c in l_ ] ) :
            if not do_one :
                pass
            else :
                do_one = 0
                res_.append(res[il])
        else :
            do_one = 1
            res_.append(res[il])
    res = res_[:]
    res = [ norm(COLUMNS-2, e, force=0, shift=int(environ["HY_SHIFT"])) for e in res ]
    if environ["HY_REVERSE"]=="1" : res = list(reversed(res))
    nn = u''
    if environ["HY_CLUSTER_TTY"]=="0" : 
        out = u"\033[0;37m│ "+(u"\033[0;37m\n\033[0;37m│ \033[0;37m").join(res) + u"\033[0;37m"+u"\n\033[0;37m│%s\n\033[0;37m│\n"%print_root
    else :
        out = u"\033[0;37m│ "+(u"\033[0;37m\n\033[0;37m│ \033[0;37m").join(res) + u"\033[0;37m"+u"\n\033[0;37m│%s\n\033[0;37m│\n"%print_root
    out = out.replace('\0',' ').replace('\1','+').replace('\2','.').replace('\3','^').replace('\4','?').replace('\5','*').replace('\6','!')
    out = out.encode('utf8') # necessaire pour sortie par PS1
    if environ["HY_TRUE_COLORS"]=="256" : out = color_24bit_to_8bit(out)
    return out


def regroup(nest, odict) :
    new_nest = []
    treated = []
    for ie,e in enumerate(nest) :
        e_unspaced = sub('(?<!\\\) ', '' ,e)
        if e_unspaced  not in treated :
            new_nest.append([(e, odict[e_unspaced], e_unspaced)])
            treated.append(e_unspaced)
        for je, f in enumerate(nest[ie+1:]) :
            f_unspaced = sub('(?<!\\\) ', '' ,f)
            if f_unspaced and ( e_unspaced==f_unspaced or match("^"+e_unspaced+"/.*", f_unspaced) or match("^"+f_unspaced+"/.*", e_unspaced) ) and (f_unspaced not in treated) :
                new_nest[-1].append((f, odict[f_unspaced], f_unspaced))
                treated.append(f_unspaced)
    sorted_nest_groups = [ sorted(g, key=lambda e: len(e[2]), reverse=True) for g in new_nest ]
    return [ [ (s[0], s[1]) for s in g ] for g in sorted_nest_groups ]

def simple_space_paths(llist, spacer):
    llist_orig = llist[:]
    llist_orig_sorted = sorted([ (e, i) for i,e in enumerate(llist_orig)], key=lambda e: e[0].count('/'), reverse=True)
    llist_orig_sorted_indexes = [ t[1] for t in llist_orig_sorted ]
    new_llist = []
    shortened_path_dict, original_path_dict = {}, {}
    for il in range(len(llist)) :
        l = llist[llist_orig_sorted_indexes[il]]
        unspaced_l = l[:]
        for ill in range(len(llist)) :
            ll = llist[llist_orig_sorted_indexes[ill]]
            if ll.startswith(l+'/') :
                ll_split = ll.split('/')
                st = len(l.split('/'))
                spaced_ll = (u'/'.join(ll_split[:st]))+(u' '*(spacer-len(ll_split[st-1]))) + u'/'+(u'/'.join(ll_split[st:]))
                llist[llist_orig_sorted_indexes[ill]] = spaced_ll
            else :
                spaced_ll = ll
            shortened_path_dict[spaced_ll.rstrip()] = spaced_ll
            original_path_dict[spaced_ll.rstrip()] = ll
    return llist, shortened_path_dict, original_path_dict

def space_paths(llist, compact_paths, COLUMNS, spacer, odict):#, hdepth=0):
    shortened_path_dict = {}
    original_path_dict = {}
    llist_orig = llist[:]
    llist_orig_sorted = sorted([ (e, i) for i,e in enumerate(llist_orig)], key=lambda e: e[0].count('/'))
    llist_orig_sorted_indexes = [ t[1] for t in llist_orig_sorted ]
    for il in range(len(llist)) :
        l_orig = llist_orig_sorted[il][0]
        l = llist[llist_orig_sorted_indexes[il]]
        l_split = l.split(' ')
        l_split_filtered = [ e for e in l_split if e ]
        last_split = l_split[-1]
        max_last_split_len = COLUMNS
        spaced_l = l+(" "*(spacer-len(last_split)))
        shortened_path_dict[spaced_l.rstrip()] = spaced_l
        original_path_dict[spaced_l.rstrip()] = l_orig
        for ill in range(il+1, len(llist)) :
            ll = llist[llist_orig_sorted_indexes[ill]]
            if ll.startswith(l+'/') :
                res = spaced_l+ll[len(l):]
                llist[llist_orig_sorted_indexes[ill]] = res
                long_path = sub('(?<!\\\) ', '' , llist_orig_sorted[ill][0] )
                tmp = odict[long_path]
    for il in range(len(llist)) :
        l = llist[il]
        l_split = re_split('(?<!\\\) ', l)
        if l_split[-1]!=u'' :
            llist[il] = llist[il]+(" "*(spacer-len(l_split[-1])))
            pass
    return llist, shortened_path_dict, original_path_dict

def calc_auto_space(alist, COLUMNS, spacer, sep='/'):
    new = {}
    if sep==' /' :
        for ie, e in enumerate(alist) :
            for iee, ee in enumerate(alist) :
                if e==ee : continue
                if e in ee :
                    ee = ee.replace(e, e+'    ')
                if ee in e :
                    e = e.replace(ee, ee+'    ')
                new[ee] = ee
                new[e] = e
        if new.keys() : alist = new.keys()
    shift = 0
    v = 0
    if sep=='/' : shift = 1
    max_nb_slash = max([ e.count(sep)-shift for e in alist ])+1
    if max_nb_slash in (0,1) : auto_spacer = COLUMNS-3
    else               : auto_spacer = (COLUMNS-3)/max_nb_slash
    spacer = auto_spacer
    return spacer

def read_from_env_or_file(filename, env_var) :
    ret = environ[env_var]
    if not ret :
        opp = open(filename, 'r')
        rd = opp.readlines()
        opp.close()
        if rd :
            ret = rd[0]
        else :
            ret = ''
    return ret

def write_to_env_or_file(filename, env_var) :
    ret = environ["env_var"]
    if not ret :
        opp = open(filename, 'r')
        rd = opp.readlines()
        opp.close()
        if rd :
            ret = rd[0]
        else :
            ret = ''
    return ret


def tree_main(i_tty, spacer, __argv__, LINES, COLUMNS) :
    spacer_ini = spacer
    nest, flat, treated = [], [], []
    #opp = open(HOME+"/.hydrix/history/root.%i"%i_tty, 'r')
    #rd = opp.readlines()
    #opp.close()
    #if rd :
        #root = rd[0]
    #else :
        #root = ''
    root = read_from_env_or_file(HOME+"/.hydrix/history/root.%i"%i_tty, "HY_ROOT")
    nb_h_lines = int(environ["HY_LINES"])
    if len(__argv__)==6:
        hgrep = ''
        filter_time = None
    else :
        rest = ' '.join(__argv__[6:])
        _srch = search('([^\~]*\ )?((?:[0-9]+[jhm])?~(?:[0-9]+[jhm])?)(.*)', rest)
        if _srch :
            filter_time = _srch.groups()[1]
            if _srch.groups()[0] : hgrep = _srch.groups()[0]
            else                 : hgrep = _srch.groups()[2]
        else :
            filter_time = None
            hgrep = rest
    hgrep = hgrep.strip()
    highlight_col = _color_tty(0, 0, __argv__)
    opp = open(HOME+"/.hydrix/history/head.%i"%i_tty, 'r')
    rdd = opp.readlines()
    opp.close()
    if ( len(rdd)==1 and int(__argv__[5])==0 ) :
        head = rdd[0].decode('utf8', 'replace')
    else :
        head = expanduser(getcwd()).decode('utf8', 'replace')
        opp = open(HOME+"/.hydrix/history/head.%i"%i_tty, 'w')
        opp.write("%s\n"%head.encode('utf8'))
        opp.close()
    hy_cd = ''
    if hy_cscope :
        hy_cd = environ["HY_CD"]
    head = head.strip()
    odict, max_mark, print_root = eagle(i_tty, 5, 1, COLUMNS, root, nb_h_lines, hgrep, highlight_col, hy_cd, filter_time=filter_time)
    llist = odict.keys()
    llist_orig = llist[:]
    if llist==[] :
        print '│[]'
        print "\033[0;00m"
        exit()
    compact_paths = int(environ["HY_COMPACT"])
    if spacer==-1 : spacer = calc_auto_space(llist_orig, COLUMNS, spacer, sep='/')
    _llist = []
    llist_orig_sorted = sorted([ (e, i) for i,e in enumerate(llist)], key=lambda e: e[0].count('/'), reverse=True)
    llist_orig_sorted_indexes = [ t[1] for t in llist_orig_sorted ]
    def pos_or_null(e) :
        if e>0 : return e
        else   : return 0
    shortened_path_dict, original_path_dict = {}, {}
    for il,elt in enumerate(llist) :
        l = llist[llist_orig_sorted_indexes[il]]
        l_split = l.split('/')
        spaced_l = (u'/'.join(l_split[:-1]))+u'/'+l_split[-1]+(u' '*pos_or_null(spacer-len(l_split[-1])))
        for ill in range(len(llist)) :
            ll = llist[llist_orig_sorted_indexes[ill]]
            if match("^"+l+"(/.*|$)", ll) :
                ll_split = ll.split('/')
                spaced_ll = ll.replace(l, spaced_l)
                llist[llist_orig_sorted_indexes[ill]] = spaced_ll
            else :
                spaced_ll = ll
            shortened_path_dict[spaced_ll.rstrip()] = spaced_ll
            original_path_dict[spaced_ll.rstrip()] = ll
    flat = llist_orig[:]
    flat, treated, nest = build_recursive_nest(head, flat, treated, nest, llist_orig, level=0)
    nest_prime = nest[:]
    nest = [ llist[llist_orig.index(n)] for n in nest if n.strip()!=u'']
    sorted_nest_groups = regroup(nest, odict)
    filtered_sorted_nest_groups = sorted_nest_groups
    res = split_blocks(filtered_sorted_nest_groups, odict, __argv__, spacer_ini, shortened_path_dict, max_mark, COLUMNS, nb_h_lines, highlight_col, original_path_dict, print_root)
    return res

def run(__argv__):
    global HOME, verb
    if environ["HY_CLUSTER_TTY"]=='0' : BAR = '\033[37m│'
    else                             : BAR = '\033[7;37m│\033[0;37m'
    verb = 0
    get_term_size = 1
    if get_term_size : COLUMNS, LINES = getTerminalSize()
    else : COLUMNS, LINES = int(environ["COLUMNS"]), int(environ["LINES"])
    if '/' in __argv__[1] :
        i_tty = int(__argv__[1].split('/')[-1])
    else :
        i_tty = int(__argv__[1][0:])
    spacer = int(__argv__[2])
    print '\033[37m'+str(i_tty),
    res = tree_main(i_tty, spacer, __argv__, LINES, COLUMNS)
    if not res.strip() :
        print "not res.strip()"
        if verb : print '\033[37m│not res.strip()'
        else    : print BAR
    else :
        print res


if __name__=='__main__' :
    run(argv)
    print "\033[0;00m"
