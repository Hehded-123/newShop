from django.forms import ModelForm, TextInput, EmailInput, Textarea
from .models import Contact



class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        
        widgets ={
            'name': TextInput(attrs={'placeholder': 'Your name'}),
            'email': TextInput(attrs={'placeholder': 'Email'}),
            'phone': TextInput(attrs={'placeholder': 'Phone'}),
            'message': TextInput(attrs={'placeholder': 'Message'}),
        }
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
