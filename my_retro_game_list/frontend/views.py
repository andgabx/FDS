from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User, Game


##############################
# Cadastro de novos usuários #
##############################

class CadastroView(View):
    
    def get(self, request):
        return render(request, 'cadastro.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Basic validation
        if not username or not email or not password:
            messages.error(request, 'Please, fill all fields.')
            return redirect('cadastro')

        try:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'User registered!')
            return redirect('login')
        
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('cadastro')  # Redirect back to the registration page on error
    

####################
# Login de usuário #
####################

class LoginView(View):

    # Método que lida com as requisições GET e exibe o formulario de login
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('')
            else:
                messages.error(request, 'Error during login! Check your credentials.')
                return redirect('login')
        except Exception as e:
            messages.error(request, f'Error during login: {str(e)}')
            return redirect('login')


################################
#  Mostrar perfis de usuário   #
################################

class ExternalUserProfileDisplayView(View):
    def get(self, request, id):
        context = { 'user' : User.objects.get(id=id), }
        return render(request, 'external_profile.html', context)


################
#  ADICIONAR   #
################

class ManageGameAdditionView(View):
    def post(self, request, action, id):
        game = get_object_or_404(Game, id=id)

        if action == 'add_to_playing_now':
            request.user.add_to_playing_now(game.id)
            return JsonResponse({'success': True, 'message': 'Game added to Playing Now list.'})

        elif action == 'add_to_to_play':
            request.user.add_to_to_play(game.id)
            return JsonResponse({'success': True, 'message': 'Game added to To Play list.'})

        elif action == 'add_to_already_played':
            request.user.add_to_already_played(game.id)
            return JsonResponse({'success': True, 'message': 'Game added to Already Played list.'})

        elif action == 'add_to_favorite_list':
            request.user.add_to_favorite_list(game.id)
            return JsonResponse({'success': True, 'message': 'Game added to Favorite list.'})

        else:
            return JsonResponse({'success': False, 'message': 'Invalid action.'}, status=400)


###########
# REMOVER # 
###########

class ManageGameRemovalView(View):
    def post(self, request, action, id):
        game = get_object_or_404(Game, id=id)

        if action == 'remove_from_playing_now':
            request.user.remove_playing_now(game.id)
            return JsonResponse({'success': True, 'message': 'Game removed from Playing Now list.'})

        elif action == 'remove_from_already_played':
            request.user.remove_from_already_played(game.id)
            return JsonResponse({'success': True, 'message': 'Game removed from Already Played list.'})

        elif action == 'remove_from_to_play':
            request.user.remove_from_to_play(game.id)
            return JsonResponse({'success': True, 'message': 'Game removed from To Play list.'})

        elif action == 'remove_from_favorite_list':
            request.user.remove_from_favorite_list(game.id)
            return JsonResponse({'success': True, 'message': 'Game removed from Favorite list.'})

        else:
            return JsonResponse({'success': False, 'message': 'Invalid action.'}, status=400)
        


####################
#       HOME       #
####################

class HomeView(View):
    def get(self, request):
        context = {
            'top_to_play': Game.top_4_to_play(),
            'top_favorites': Game.top_4_favorite_list(),
            'top_playing_now': Game.top_4_playing_now(),
            'top_already_played': Game.top_4_already_played(),
            'user': request.user,
        }
        return render(request, 'home.html', context)