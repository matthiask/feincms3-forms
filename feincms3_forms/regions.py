from hashlib import sha1

from feincms3.regions import Regions


class FormRegions(Regions):
    def get_form(self, *, region, form_class, form_kwargs):
        item_fields = {}
        all_fields = {}
        initial = form_kwargs.setdefault("initial", {})

        if items := self.contents[region]:
            parent = items[0].parent
            identifier = f"{parent._meta.model_name}-{parent.id}-{items[0].region}"
            form_kwargs["prefix"] = sha1(identifier.encode("utf-8")).hexdigest()[:6]

            for item in items:
                if hasattr(item, "get_fields"):
                    item_fields[item] = fields = item.get_fields(initial=initial)
                    all_fields.update(fields)

        form_kwargs.setdefault("auto_id", "")
        form = type("Form", (form_class,), all_fields.copy())(**form_kwargs)

        for item, fields in item_fields.items():
            item.fields = {key: form[key] for key in fields}

        form.other_fields = {
            key: form[key] for key in form.fields if key not in all_fields
        }

        return form
