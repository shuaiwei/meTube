from modelView.models import * 
from django.db.models import Q

querySet = ['man1', 'tt']

q=Media.objects.filter(keyword__contains=['man1','tt']).values_list()

q = Media.objects.filter(reduce(lambda x, y: x | y, [Q(keyword__contains=item) for item in querySet]))

q = Media.objects.filter(Q(keyword__contains=querySet[0]) | Q(keyword__contains=querySet[1]))
