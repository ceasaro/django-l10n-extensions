## TransField Model Field extension

This Django model field translates content stored in your database using the same approach as the standard django 
 translation methods like `gettext`, `pgettest`, `ngettest` and `npgexttest` 
 (see the [Django 1.11 translation](https://docs.djangoproject.com/en/1.11/topics/i18n/translation/))
 
To Collect the messages of the `TransField` stored in the database simply run: 
  
  `python manage.py makemessages`
 
__!NOTE__ This is not meant to translate user generated content, it's more suitable for static text stored in a database.
Think of a list of products or some definition list that needs to be translated. There are other libraries probably more 
suitable for translating user generated content take a look a these 
[libraries](https://djangopackages.org/grids/g/model-translation/).
   
### simple text 
_equivalent to Django's `gettext(message)`_

```python
title = TransField(max_length=128)
```

The string from the title model field will be translated like any message passed through the Django's `gettext()` method.
Below a complete example:
```python   
class Product(models.Model):
    name = TransField(max_length=128)

product = Product(name='Spring')
product.name → 'Spring'

activate('nl')

product.name → 'Lente'
```      


### translate with context 
_Equivalent to Django's `pgettext(context, message)`_

You can use the same `TransField` as above but pass in an extra context message.
```python
class Product(models.Model):
    name = TransField(max_length=128)

product = Product(name=('mechanical device', 'spring'))  # pass in a tuple (context, message)
product.name → 'spring'

activate('nl')

product.name → 'veer'  # not Lente cause the context says it's a mechanical device!
```

### translate plural 
_equivalent to Django's `pgettext(singular, plural)`_

You can still use the same `TransField` as the above examples, but the argument passed to the field has now a dict style.
```python
class Product(models.Model):
    name = TransField(max_length=128)

product = Product(name={'msgid':'car', 'plural':'cars'})  # pass in a T9N dict
product.name.trans(0) → 'cars'
product.name.trans(1) → 'car'
product.name.trans(4) → 'cars'

activate('nl')

product.name.trans(0) → 'autos' 
product.name.trans(1) → 'auto' 
product.name.trans(4) → 'autos' 
```

### translate plural with context 
_equivalent to Django's `ngettext(context, singular, plural)`_

We still use the same `TransField` as the above examples :-), and pass in dict style argument.
```python
class Product(models.Model):
    name = TransField(max_length=128)

product = Product(name={'msgid':'spring', 'plural':'springs', 'msgctxt': 'mechanical device'})  # pass in a T9N dict
product.name.trans(0) → 'springs'
product.name.trans(1) → 'spring'
product.name.trans(4) → 'springs'

activate('nl')

product.name.trans(0) → 'veren' 
product.name.trans(1) → 'veer' 
product.name.trans(4) → 'veren' 
```

## Make the messages.
To make the messages, that is add the messages stored in the database to the po file so they can be translated, you can 
use the same Django management command: `makemessages`

`python manage.py makemessages`

Running this command will work the same as the original Django's `makemessages` command but as an addition aslo collects all 
messages from the `TransField` model fields and add them to your po file.

If you need to run the original `makemessages` command without colleting the `TransField` messages pass in the following 
option:

`python manage.py makemessages --no-models`

If you which to only collect the messages of the `TransField` model fields run:

`python manage.py makemessages --models-only`
