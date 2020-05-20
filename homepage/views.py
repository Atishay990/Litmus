from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .models import Notes
from litmus.models import Profile

# View for /homepagedemo/
def index(request):
    if request.user.is_authenticted:
        try:
            # Select most popular notes from the notes of user's friends 
            pass

        except(KeyError, Notes.DoesNotExist):
            popularnote = 'No notes yet! Go ahead and create your first note !'
            return render(request, 'homepage/notes2.html', 
                         {'popularnote': popularnote})
        else:
            # Passing selected note tobe displayed on basic HTML page
            return render(request, 'homepage/notes2.html', 
                         {'popularnote': popularnote})

# View for # /homepagedemo/addnotes/
def add(request):
    # Saving newly added notes from the homepage 
    newnote = request.POST.get("newnote")
    is_public = request.POST.get("is_public")
    print(newnote)
    #if newnote == "":
        #return redirect(errors, error_code = 400)
        #return render(request, 'homepage/homepageerror.html', 
        #            {'error_message' : error_message,})
    #else:

    n = Notes()
    n.user_profile = request.user
    n.diary_notes = newnote
    n.is_public = is_public
    n.save()
    latestnote = n.diary_notes
    return redirect('/litmus/homepagedemo/' + str(user_id) + '/')

# Error messages
def errors(request, error_code):
    print("Hey here\n\n")
    return render(request, 'homepage/homepageerror.html', 
                 {'error_code' : error_code,})   
  