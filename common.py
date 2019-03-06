def getTerminalSize():
    from os import environ
    env = environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct
            from termios import TIOCGWINSZ
            from struct import unpack
            from fcntl import ioctl
            from os import O_RDONLY, ctermid
            cr = unpack('hh', ioctl(fd, TIOCGWINSZ, '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = open(ctermid(), O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            close(fd)
        except:
            pass
    if not cr:
        cr = (environ.get('LINES', 25), environ.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])
