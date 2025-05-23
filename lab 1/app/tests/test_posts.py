from contextlib import contextmanager
from flask import template_rendered
from datetime import datetime
from unittest.mock import patch
from app import posts_list

# Test 1
def test_posts_index(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert "Последние посты" in response.text

# Test 2
def test_posts_index_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.posts_list",
            return_value=posts_list,
            autospec=True
        )
        
        _ = client.get('/posts')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        assert context['title'] == 'Посты'
        assert len(context['posts']) == 1

# Test 3
def test_posts_list_context(client):
    with captured_templates(client.application) as templates:
        client.get("/posts")
        context = templates[0][1]
        assert "posts" in context
        assert isinstance(context["posts"], list)

# Test 4
def test_post_detail_rendering(client, mocker):
    test_post = {
        'title': 'Sample Post',
        'text': 'Post content here',
        'author': 'John Doe',
        'date': datetime(2023, 5, 15),
        'image_id': 'sample.jpg',
        'comments': []
    }
    mocker.patch('app.posts_list', return_value=[test_post])
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'Sample Post' in response.text

# Test 5
def test_post_image_display(client):
    test_post = {
        'title': 'Image Test',
        'text': 'Check the image',
        'author': 'Photographer',
        'date': datetime.now(),
        'image_id': 'photo.jpg',
        'comments': []
    }
    with patch('app.posts_list', return_value=[test_post]):
        response = client.get('/posts/0')
        assert 'src="/static/images/photo.jpg"' in response.text

# Test 6
def test_comment_form_presence(client):
    test_post = {
        'title': 'Comment Test',
        'text': 'Test post',
        'author': 'Author',
        'date': datetime.now(),
        'image_id': 'test.jpg',
        'comments': []
    }
    with patch('app.posts_list', return_value=[test_post]):
        response = client.get('/posts/0')
        assert 'Оставьте комментарий' in response.text
        assert '<form' in response.text

# Test 7
def test_invalid_post_id(client, mocker):
    mocker.patch('app.posts_list', return_value=[])
    response = client.get('/post/999')
    assert response.status_code == 404

# Test 8
def test_post_date_display(client):
    test_post = {
        'title': 'Date Test',
        'text': 'Testing date format',
        'author': 'Timekeeper',
        'date': datetime(2023, 12, 25),
        'image_id': 'holiday.jpg',
        'comments': []
    }
    with patch('app.posts_list', return_value=[test_post]):
        response = client.get('/posts/0')
        assert '25.12.2023' in response.text

# Test 9
def test_nested_comments(client):
    test_post = {
        'title': 'Nested Comments',
        'text': 'Main content',
        'author': 'OP',
        'date': datetime.now(),
        'image_id': 'main.jpg',
        'comments': [{
            'author': 'First',
            'text': 'Top level',
            'date': datetime.now(),
            'time': '12:24:11',
            'replies': [{
                'author': 'Second',
                'text': 'Reply here',
                'date': datetime.now(),
                'time': '12:24:11'
            }]
        }]
    }
    with patch('app.posts_list', return_value=[test_post]):
        response = client.get('/posts/0')
        assert 'Top level' in response.text
        assert 'Reply here' in response.text

# Test 10
def test_comment_avatars_appear(client):
    test_post = {
        'title': 'Avatar Test',
        'text': 'Check avatars',
        'author': 'User',
        'date': datetime.now(),
        'image_id': 'post.jpg',
        'comments': [{
            'author': 'Commenter',
            'text': 'With avatar',
            'date': datetime.now(),
            'time': '12:24:11',
            'replies': []
        }]
    }
    with patch('app.posts_list', return_value=[test_post]):
        response = client.get('/posts/0')
        assert 'avatar.jpg' in response.text

# Test 11
def test_long_post_truncation(client, mocker):
    long_text = "This is a very long post text that should be truncated in the list view " * 5
    test_post = {
        'title': 'Long Post',
        'text': long_text,
        'author': 'Writer',
        'date': datetime.now(),
        'image_id': 'book.jpg',
        'comments': []
    }
    mocker.patch('app.posts_list', return_value=[test_post])
    response = client.get('/posts')
    assert '...' in response.text

# Test 12
def test_post_links_in_list_view(client):
    test_posts = [
        {
            'title': f'Post {i}',
            'text': f'Content {i}',
            'author': f'Author {i}',
            'date': datetime.now(),
            'image_id': f'img{i}.jpg',
            'comments': []
        }
        for i in range(3)
    ]
    with patch('app.posts_list', return_value=test_posts):
        response = client.get('/posts')
        for i in range(3):
            assert f'href="/posts/{i}"' in response.text

# Test 13
def test_post_detail_template_used(client):
    test_post = {
        'title': 'Template Test',
        'text': 'Template check',
        'author': 'Tester',
        'date': datetime.now(),
        'image_id': 'test.jpg',
        'comments': []
    }
    with patch('app.posts_list', return_value=[test_post]):
        with captured_templates(client.application) as templates:
            client.get('/posts/0')
            assert templates[0][0].name == 'post.html'

# Test 14
def test_multiple_comments_rendering(client):
    test_post = {
        'title': 'Multi-Comment',
        'text': 'Many comments',
        'author': 'Poster',
        'date': datetime.now(),
        'image_id': 'multi.jpg',
        'comments': [
            {
                'author': f'User {i}',
                'text': f'Comment {i}',
                'date': datetime.now(),
                'time': '12:24:11',
                'replies': []
            }
            for i in range(5)
        ]
    }
    with patch('app.posts_list', return_value=[test_post]):
        response = client.get('/posts/0')
        for i in range(5):
            assert f'Comment {i}' in response.text

# Test 15
def test_post_title_context(client):
    with captured_templates(client.application) as templates:
        client.get("/posts")
        context = templates[0][1]
        assert context["title"] == "Посты"

@contextmanager
def captured_templates(app):
    templates = []
    def record(sender, template, context, **extra):
        templates.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield templates
    finally:
        template_rendered.disconnect(record, app)
