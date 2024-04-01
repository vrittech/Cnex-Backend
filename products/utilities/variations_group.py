from variations.models import VariationOption

def ArrangeVariationGroup(variations):
    variations1 =    [
        {
            "variation": "color",
            "variation_id": 2,
            "variation_option_value": "yellow",
            "variation_value_id": 3,
            "price": 787.0,
            "quantity": 1
        },
        {
            "variation": "size",
            "variation_id": 1,
            "variation_option_value": "XL",
            "variation_value_id": 7,
            "price": 98.0,
            "quantity": 1
        }
    ],
    main_list = []

    main_dict = {}

    for var in variations:
        main_variations = {
            'varient_name':var.get('variation'),
            'id':var.get('variation_id'),
            'varient_option':[{
                'id':var.get('variation_value_id'),
                'name':var.get('variation_option_value'),
                'quantity':var.get('quantity'),
                'price':var.get('price'),
                'selected':True,
            }],
            'varient':{
                'id':var.get('variation_id'),
                'options':[{'id':varient.id,'value':varient.value} for varient in VariationOption.objects.filter(variation_id = var.get('variation_id'))]
            }
        }
        if main_dict.get(var.get('variation')):
            main_dict[var.get('variation')]['varient_option'].append(main_variations.get('varient_option'))
        else:
            main_dict[var.get('variation')] = main_variations
        # main_list.append(main_variations)
    for m_d in main_dict:
        main_list.append(main_dict.get(m_d))
   
    return main_list
