from django.shortcuts import render_to_response

from card.models import Card
from django.views import generic
from django.http import HttpResponseRedirect


class BusinessCard(generic.TemplateView):
    template_name = 'card/card.html'

    def post(self, request, *args, **kwargs):
        body = request.POST
        Card.objects.create(
            name=body.get('name'),
            surname=body.get('surname'),
            phone_number=body.get('phone_number'),
            topic=body.get('topic'),
            text=body.get('text')
        ).save()
        return HttpResponseRedirect('/card/')

    def get_context_data(self, **kwargs):
        ctx = super(BusinessCard, self).get_context_data(**kwargs)
        ctx['extended_form'] = True
        qs = Card.objects.all()
        if qs.__len__() != 0:
            qs = qs[0]
            ctx['card_body'] = {
                'name': qs.name,
                'surname': qs.surname,
                'phone_number': qs.phone_number,
                'topic': qs.topic,
                'text': qs.text,
                'loaded': True
            }
        else:
            ctx['card_body'] = {'loaded': False}
        return ctx


class Delete(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        Card.objects.all().delete()
        return HttpResponseRedirect('/card/')
