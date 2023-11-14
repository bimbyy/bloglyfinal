from models import Post  # Import the Post model
from flasker import db

class AppTestCase(unittest.TestCase):
    # ... (existing code)

    def test_new_post_form_route(self):
        response = self.app.get('/users/1/posts/new')  # Replace '1' with a valid user ID for testing
        self.assertEqual(response.status_code, 200)

    def test_create_post_route(self):
        user = User(first_name='Test', last_name='User', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()
        
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }
        response = self.app.post(f'/users/{user.id}/posts/new', data=data)
        self.assertEqual(response.status_code, 302)  # Should redirect to user detail page

    def test_post_detail_route(self):
        # Create a test post
        user = User(first_name='Test', last_name='User', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()
        
        post = Post(title='Test Post', content='This is a test post.', user_id=user.id)
        db.session.add(post)
        db.session.commit()
        
        response = self.app.get(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 200)

    def test_edit_post_form_route(self):
        # Create a test post
        user = User(first_name='Test', last_name='User', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()
        
        post = Post(title='Test Post', content='This is a test post.', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        response = self.app.get(f'/posts/{post.id}/edit')
        self.assertEqual(response.status_code, 200)

    def test_update_post_route(self):
        # Create a test post
        user = User(first_name='Test', last_name='User', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()
        
        post = Post(title='Test Post', content='This is a test post.', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        data = {
            'title': 'Updated Post',
            'content': 'This is an updated test post.'
        }
        response = self.app.post(f'/posts/{post.id}/edit', data=data)
        self.assertEqual(response.status_code, 302)  # Should redirect to post detail page

    def test_delete_post_route(self):
        # Create a test post
        user = User(first_name='Test', last_name='User', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()
        
        post = Post(title='Test Post', content='This is a test post.', user_id=user.id)
        db.session.add(post)
        db.session.commit()
        
        response = self.app.post(f'/posts/{post.id}/delete')
        self.assertEqual(response.status_code, 302)  # Should redirect to user detail page
