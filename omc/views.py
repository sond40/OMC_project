from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Recipe, CategoryT, CategoryS, CategoryI, CategoryM, RecipeOrder, Ingredient, RecipeHashTag, UserIngredient
# from .forms import CategoryForm

# Create your views here.
def index(requests):
    # recipe = recipe.objects.all().order_by("-")
    return render(requests,"index.html")


class RecipeList(ListView):
    model = Recipe
    paginate_by = 40
    template_name = 'omc/recipe_list_view.html'
    ordering='pk'

    def get_context_data(self, **kwargs):
        context = super(RecipeList, self).get_context_data(**kwargs)

        if not context.get('is_paginated', False):
            return context

        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number

        if num_pages <= 11 or page_no <= 6:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page_no > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 5, page_no + 6)]

        context.update({'pages': pages})

        context['category_t'] = CategoryT.objects.all()
        context['category_s'] = CategoryS.objects.all()
        context['category_i'] = CategoryI.objects.all()
        context['category_m'] = CategoryM.objects.all()

        return context

class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'omc/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RecipeDetail,self).get_context_data()
        context['ingredients'] = Ingredient.objects.filter(recipeId=context['recipe'].pk)
        context['ingredients_types'] = Ingredient.objects.filter(recipeId=context['recipe'].pk).values_list('type').distinct().values('type')
        context['recipehastags'] = RecipeHashTag.objects.filter(recipeId=context['recipe'].pk)
        context['recipe_order'] = RecipeOrder.objects.filter(recipeId=context['recipe'].pk)
        if context['recipe'].categoryTId != None:
            context['category_t'] = CategoryT.objects.get(pk=context['recipe'].categoryTId_id)
            context['category_s'] = CategoryS.objects.get(pk=context['recipe'].categorySId_id)
            context['category_i'] = CategoryI.objects.get(pk=context['recipe'].categoryIId_id)
            context['category_m'] = CategoryM.objects.get(pk=context['recipe'].categoryMId_id)
        return context

class RefrigeratorList(TemplateView):
    template_name = 'omc/refrigerator_list_view.html'
    
    def get_context_data(self, **kwargs):
        context = super(RefrigeratorList, self).get_context_data()
        context['ingredients'] = UserIngredient.objects.all()
        context['ingredients_types'] = UserIngredient.objects.all().values_list('type').distinct().values('type')
        return context

class RecipeSearch(RecipeList):
    paginate_by = 40
    # paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']

        recipe_id_list = set()
        recipe_lst = Recipe.objects.filter(name__contains=q).distinct()
        for recipe in recipe_lst:
            recipe_id_list.add(recipe.pk)

        recipe_lst = Ingredient.objects.filter(name__contains=q).distinct()
        for recipe in recipe_lst:
            recipe_id_list.add(recipe.recipeId.pk)
        
        recipe_lst = RecipeOrder.objects.filter(description__contains=q).distinct()
        for recipe in recipe_lst:
            recipe_id_list.add(recipe.recipeId.pk)
        
        recipe_lst = RecipeHashTag.objects.filter(description__contains=q).distinct()
        for recipe in recipe_lst:
            recipe_id_list.add(recipe.recipeId.pk)

        recipe_id_list = list(recipe_id_list)
        recipe_list = Recipe.objects.filter(pk__in=recipe_id_list)

        return recipe_list

    def get_context_data(self, **kwargs):
        context = super(RecipeSearch, self).get_context_data(**kwargs)

        if not context.get('is_paginated', False):
            pages = [1]
        else:
            paginator = context.get('paginator')
            num_pages = paginator.num_pages
            current_page = context.get('page_obj')
            page_no = current_page.number

            if num_pages <= 11 or page_no <= 6:  # case 1 and 2
                pages = [x for x in range(1, min(num_pages + 1, 12))]
            elif page_no > num_pages - 6:  # case 4
                pages = [x for x in range(num_pages - 10, num_pages + 1)]
            else:  # case 3
                pages = [x for x in range(page_no - 5, page_no + 6)]
            
        context.update({'pages': pages})
        context['category_t'] = CategoryT.objects.all()
        context['category_s'] = CategoryS.objects.all()
        context['category_i'] = CategoryI.objects.all()
        context['category_m'] = CategoryM.objects.all()
        
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        context['search_word'] = q
        return context
