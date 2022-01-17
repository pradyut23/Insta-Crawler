from application import app
from flask import render_template, redirect, url_for, flash
from application.forms import AnonymousForm, LoginForm
from instaloader import Instaloader, Profile
from instagramy import InstagramUser

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html', index = True)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data

        if user and password:
            try:
                instag = Instaloader()
                instag.login(user, password)
                instag.save_session_to_file()
                return redirect(url_for('loginprofile', username=user))
            except:
                flash('Wrong Credentials. Please Try Again!!', 'danger')
    return render_template('login.html', title='Login', form = form, login = True)


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    form = AnonymousForm()
    if form.validate_on_submit():
        userID = form.userID.data
        print(userID)
        return redirect(url_for('anonymous', userID=userID))
    return render_template('profile.html', form = form, profile = True)


@app.route('/loginprofile')
@app.route('/<username>', methods=['POST', 'GET'])
def loginprofile(username = None):
    try:
        instag = Instaloader()
        instag.load_session_from_file(username)
        form = AnonymousForm()
        if form.validate_on_submit():
            userID = form.userID.data
            return redirect(url_for('loggedin', username=username, profile=userID))
        return render_template('profile.html', form=form, loginprofile = True)
    except:
        return redirect(url_for('login'))


@app.route('/loggedin')
@app.route('/<username>/<profile>')
def loggedin(username = None, profile = None):
    instag = Instaloader()
    instag.load_session_from_file(username)
    profile = Profile.from_username(instag.context, profile)

    followers_list = []
    verified_followers_list = []
    follower_iterator = profile.get_followers()
    posts = profile.get_posts()
    post_data = []
    for follower in follower_iterator:
        followers_list.append(follower.username)
        if follower.is_verified:
            verified_followers_list.append(follower.username)

    count = 0
    for post in posts:
        a = {'Post': count+1, 'Likes': post.likes, 'Comments': post.comments}
        count+=1
        post_data.append(a)
        if count == 11:
            break

    return render_template('loggedin.html', userID=profile, verified=profile.is_verified, name=profile.full_name, bio=profile.biography, posts=profile.mediacount, following=profile.followees, followers=profile.followers, pic=profile.profile_pic_url, followers_list = followers_list, verified_followers_list = verified_followers_list, post_data = post_data, loggedin = True)


@app.route('/anonymous/<userID>')
def anonymous(userID = None):
    user = InstagramUser(userID, from_cache=True)
    user_data = user.user_data
    name = user.fullname
    bio = user.biography
    if not user_data['is_private']:
        verified = user.is_verified
        following = user.number_of_followings
        followers = user.number_of_followers
        posts = user.number_of_posts
        reels = user_data['highlight_reel_count']
        category = user_data['category_name']
        profile_pic = user_data['profile_pic_url_hd']
        return render_template('anonymous.html', userID=userID, verified=verified, category=category, reels=reels, name=name, bio=bio, posts=posts, following=following, followers=followers, pic=profile_pic)
    else:
        flash('Please login to view a followed Private Profile!!', 'warning')
        return render_template('anonymous.html', name=name, bio=bio, pic=None)
