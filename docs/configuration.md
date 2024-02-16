## Configuration

### Fastapi/Starlette
You can configure the loading the l10n instance to be used from the starlette context,
before falling back on the threadlocal.
To  do this, add the following setting to the Django settings:
```python
L10N_STORE = 'starlette_l10n_store'
```
This will cause the threading to first check the starlette context for a l10n instance with the key "l10n_instance".
Implement a plugin (https://starlette-context.readthedocs.io/en/latest/plugins.html) that sets this based on the user preferences.


### Default l10n
To override the default l10n, add something like the following in Django settings:
```python
DEFAULT_L10N_CONFIG = dict(
    unit_distance="m",
    unit_area="ha",
    unit_weight="g",
    unit_volume="l",
    unit_temp="C",
    unit_velocity="mps",
    unit_precipitation="mm"
)
```
