DESTDIR=/usr/

all:


install:
	install -m 755 -d $(DESTDIR)/share/delvj/
	install -m 755 -d $(DESTDIR)/share/delvj/interfazweb/
	install -m 755 -d $(DESTDIR)/share/delvj/parches/
	install -m 755 -d $(DESTDIR)/share/delvj/scripts/
	install -m 755 -d $(DESTDIR)/share/delvj/sprites/
	install -m 755 -d $(DESTDIR)/share/delvj/textos/
	install -m 755 -d $(DESTDIR)/share/delvj/glade/
	install -m 755 -d $(DESTDIR)/share/delvj/cal3d/
	install -m 755 -d $(DESTDIR)/share/delvj/cal3d/cubes/
	install -m 755 -d $(DESTDIR)/share/delvj/cal3d/logo_delvj/
	install -m 755 -d $(DESTDIR)/share/delvj/interfazweb/images/
	install -m 755 -d $(DESTDIR)/share/delvj/interfazweb/thumbsvideo/
	install -m 755 -d $(DESTDIR)/share/locale/es/LC_MESSAGES/
	install -m 755 -d $(DESTDIR)/share/locale/ca/LC_MESSAGES/
	install -m 755 -d $(DESTDIR)/share/locale/fr/LC_MESSAGES/
	install -m 755 -d $(DESTDIR)/bin/
	install -m 755 bin/* $(DESTDIR)/bin/
	install -m 644 parches/* $(DESTDIR)/share/delvj/parches/
	install -m 644 interfazweb/*php $(DESTDIR)/share/delvj/interfazweb/
	install -m 755 scripts/* $(DESTDIR)/share/delvj/scripts/
	install -m 755 sprites/* $(DESTDIR)/share/delvj/sprites/
	install -m 755 textos/* $(DESTDIR)/share/delvj/textos/
	install -m 755 cal3d/cubes/* $(DESTDIR)/share/delvj/cal3d/cubes/
	install -m 755 cal3d/logo_delvj/* $(DESTDIR)/share/delvj/cal3d/logo_delvj/
	install -m 644 glade/*png glade/*glade $(DESTDIR)/share/delvj/glade/
	install -m 755 glade/*py $(DESTDIR)/share/delvj/glade/
	install -m 644 interfazweb/images/* $(DESTDIR)/share/delvj/interfazweb/images/
	install -m 644 po/es.mo $(DESTDIR)/share/locale/es/LC_MESSAGES/delvj.mo
	install -m 644 po/ca.mo $(DESTDIR)/share/locale/ca/LC_MESSAGES/delvj.mo
	install -m 644 po/fr.mo $(DESTDIR)/share/locale/fr/LC_MESSAGES/delvj.mo
	ln -s $(DESTDIR)/share/delvj/interfazweb/ $(DESTDIR)/../var/www/delvj


