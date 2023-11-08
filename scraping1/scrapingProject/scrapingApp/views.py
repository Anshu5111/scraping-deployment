from . import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup
from scrapingApp.models import MovieInfo, UserProfileInfo
from scrapingApp.forms import newUserForm


# Create your views here.

def index(request):
    return render(request, 'scrapingApp/index.html')


@login_required()
def special(request):
    return HttpResponse("You are logged in!")


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        print(username)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return render(request, 'scrapingApp/movie.html', {})
            # return HttpResponseRedirect(reverse('movie'))
        else:
            print("Someone tried to login and failed!")
            print(f"username:{username} and password:{password}")
            return HttpResponse('Invalid login!')
    else:
        return render(request, 'scrapingApp/login.html', {})





def register(request):
    form = forms.newUserForm()
    if request.method == "POST":
        form = forms.newUserForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print("ERROR FORM INVALID")
    return render(request, 'scrapingApp/registration.html', {'form': form})



moviename=''


def outputInfo(request):
    mov = request.POST.get('moviename')
    print(mov)
    b=False
    movie=MovieInfo.objects.all()
    for a in movie:
        if mov.lower() in a.moviename.lower():
            mi=a
            b=True
    if b==False:
        return HttpResponse("Please Enter A Valid Movie Name!")
    else:
        dict={'movie':mi,'topmovies':a.topMovie}
        return render(request, 'scrapingApp/output.html',dict)

def moviename(request):
    if request.method == 'POST':
        moviename2 = request.POST.get('moviename')
        moviename2 = moviename2.lower()

        ## webscraing code

        url = 'https://www.imdb.com/chart/top/'
        res = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'})
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        ul_tag = soup.find('ul', {
            'class': 'ipc-metadata-list ipc-metadata-list--dividers-between sc-9d2f6de0-0 ckQYbL compact-list-view ipc-metadata-list--base'})
        li_tag = ul_tag.findAll('li', {'class': 'ipc-metadata-list-summary-item sc-59b6048d-0 jemTre cli-parent'})

        for list in li_tag:
            div_child = list.find('div', {'class': 'sc-c7e5f54-0 gytZrF cli-children'})
            div_tag = div_child.find('div', {
                'class': 'ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-c7e5f54-9 irGIRq cli-title'})
            anchor_tag = div_tag.find('a', {'class': 'ipc-title-link-wrapper'})
            movieTag = anchor_tag.h3
            movieName1 = movieTag.string.encode("utf-8")
            m = movieName1.decode()
            rating_tag = list.find('span', {
                'class': 'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating'})
            m_rating = rating_tag['aria-label']
            movieID = anchor_tag['href']
            movieUrl = f'https://www.imdb.com/{movieID}'
            # print(m)

            div_info = div_child.find('div', {'class': 'sc-c7e5f54-7 brlapf cli-title-metadata'})
            movieInfo = div_info.findAll('span', {'class': 'sc-c7e5f54-8 hgjcbi cli-title-metadata-item'})
            movieYear = movieInfo[0].string
            movieTiming = movieInfo[1].string
            # # print(movieUrl+'----'+movieYear+'----'+movieTiming)
            if moviename2 in m.lower():
                print("MOVIE NAME : " + m.upper())
                moviename = m.upper()
                print("MOVIE YEAR : " + movieYear)
                movieyear = movieYear
                print("MOVIE TIMING: " + movieTiming)
                movietime = movieTiming
                print("MOVIE RATING : " + m_rating)
                movierating = m_rating
                print("MOVIE URL : " + movieUrl)

                #
                #     ##
                #
                # url2='https://www.imdb.com/title/tt0111161/?ref_=chttp_t_1'
                res2 = requests.get(movieUrl, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'})
                html2 = res2.text
                soup2 = BeautifulSoup(html2, 'html.parser')
                div_tag2 = soup2.find('div', {'class': 'ipc-metadata-list-item__content-container'})
                li_tag2 = div_tag2.find('li', {'class': 'ipc-inline-list__item'})
                anch_tag2 = li_tag2.find('a')
                dirId = anch_tag2['href']
                dirName = anch_tag2.string
                dirUrl = f'https://www.imdb.com/{dirId}'
                print("MOVIE DIRECTOR NAME : " + dirName.upper())
                moviedirector = dirName.upper()
                print("MOVIE DIRECTOR URL : " + dirUrl)
                directorurl = dirUrl
                #
                #     ##
                #
                # url3='https://www.imdb.com/name/nm0001104/?ref_=tt_ov_dr'
                res3 = requests.get(dirUrl, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'})
                html3 = res3.text
                soup3 = BeautifulSoup(html3, 'html.parser')
                div_tag3 = soup3.find('div', {
                    'class': 'ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-shoveler__grid'})
                int_div_tag = div_tag3.findAll('div', {
                    'class': 'ipc-list-card--span ipc-list-card--border-line ipc-list-card ipc-primary-image-list-card ipc-primary-image-list-card--base ipc-primary-image-list-card--click sc-9cf00aac-0 dzkdTB ipc-list-card--base ipc-sub-grid-item ipc-sub-grid-item--span-4'})
                print(f'Top movies of Director {dirName.upper()} is : ')
                i = 1
                movies = []
                for div in int_div_tag:
                    div__ = div.find('div', {'class': 'ipc-primary-image-list-card__content'})
                    div_tag_final = div__.find('div', {'class': 'ipc-primary-image-list-card__content-top'})
                    anch_tag3 = div__.find('a', {'class': 'ipc-primary-image-list-card__title'})
                    movieName = anch_tag3.string
                    movies.append(movieName.upper())
                    print(f'{i}. {movieName.upper()}')
                    i = i + 1
                topmovies = movies
                # movieAll = MovieInfo.objects.all()
                # if movieAll is None:
                #     t = MovieInfo.objects.create(moviename=moviename, movieyear=movieyear, movietime=movietime,
                #                                  movieurl=movieUrl, moviedirector=moviedirector,
                #                                  movierating=movierating,
                #                                  directorurl=directorurl, topMovie=topmovies)
                #     t.save()
                #     # return render(request, 'scrapingApp/output.html', {})
                #     return outputInfo(request)
                # else:
                #     for a in movieAll:
                #         if moviename in a.moviename:
                #             return outputInfo(request)
                #             break
                #         else:
                #             t = MovieInfo.objects.create(moviename=moviename, movieyear=movieyear, movietime=movietime,
                #                                          movieurl=movieUrl, moviedirector=moviedirector,
                #                                          movierating=movierating,
                #                                          directorurl=directorurl, topMovie=topmovies)
                #             t.save()
                #             # return render(request, 'scrapingApp/output.html', {})
                #             return outputInfo(request)
                #             break
                t = MovieInfo.objects.create(moviename=moviename, movieyear=movieyear, movietime=movietime,
                                                 movieurl=movieUrl, moviedirector=moviedirector,
                                                 movierating=movierating,
                                                 directorurl=directorurl, topMovie=topmovies)
                t.save()
                # return render(request, 'scrapingApp/output.html', {})
                return outputInfo(request)
            # else:
            #     print("Please Enter correct movie name!")
            #     return render(request,'scrapingApp/movie.html')
    return render(request, 'scrapingApp/movie.html', {})

#
# def register(request):
#     if request.method == 'POST':
#         form = newUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#             username = form.cleaned_data.get('username')
#
#             password = form.cleaned_data.get('password')
#
#             user = authenticate(username=username, password=password)
#             print(user)
#             login(request, user)
#
#             return moviename(request)
#
#         else:
#
#              return render(request,'scrapingApp/registration.html', {'form': form})
#     else:
#         form = newUserForm()
#
#         return render(request, 'scrapingApp/registration.html', {'form': form})