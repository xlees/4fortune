from django.shortcuts import render,render_to_response
import sqlalchemy, sqlalchemy.orm
from sqlalchemy.orm import sessionmaker,scoped_session
from models import *
from django.conf import settings
import logging,json
from django.views.generic import View
from django.http import HttpResponse

# engine = sqlalchemy.create_engine(settings.DATABASES['default']['NAME'])
engine = sqlalchemy.create_engine('sqlite:///%s/db.sqlite3' % (settings.BASE_DIR),echo=True)
Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker(bind=engine))

logger = logging.getLogger('django')
logger.info("base_dir: "+settings.BASE_DIR)


# entrance
# def index(request):
#     if is_empty():
#         populate()

#     langs = sess.query(Language,Language.id,Language.name).all()
#     logger.debug("first elem: \t"+repr(langs[0]))

#     return render_to_response('index.html',{'langs':langs})

# entrance view
# for template rendering
class IndexView(View):
    """docstring for ClassName"""
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        self.sess = Session()

        if self.is_empty():
            self.populate()

        logger.info('type of request meta: '+repr(type(request.META)))

        langs = self.sess.query(Language,Language.id,Language.name).all()
        logger.debug("first elem: \t"+repr(langs[0]))

        self.sess.close()

        return render(request, self.template_name, {'langs':langs})

    def is_empty(self):
        l = len(self.sess.query(Language).all())
        return (l <= 0)

    def populate(self):
        new_langs = [Language('Python','py'),
                    Language('Ruby', 'rb'),
                     Language('Common Lisp', 'lisp'),
                     Language('Objective-C', 'm')]
        sess.add_all(new_langs)
        sess.commit()

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        # if form.is_valid():
            # <process form cleaned data>
            # return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {})

# for ajax request
class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        # logger.info("args: "+repr(args))
        # logger.info("kwargs: "+repr(kwargs))
        logger.info(request.GET)
        logger.info(request.GET.get("rid",90))
        logger.info(request.GET.get("name",90))
        logger.warn("greeting view!!")

        self.sess = Session()

        all_langs = self.sess.query(Language.id,Language.name).all()

        resp = {
            'code': 56,
            'msg': self.greeting,
            'langs': all_langs,
        }

        self.sess.close()

        return HttpResponse(json.dumps(resp), content_type="application/json")

