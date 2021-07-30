from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def home_view(request):
    return render(request, 'calculator/home.html')


def index_view(request, dish):
    servings = request.GET.get('servings', 1)
    recipe = DATA.get(dish)
    context = {'recipe': {key: value * int(servings) for key, value in recipe.items()}}
    return render(request, 'calculator/index.html', context)
