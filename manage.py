from app import create_app, db
from app import models
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import datetime

app = create_app()

# Init manager and migration tool
manager = Manager(app)
migrate = Migrate(app, db)


def make_context(): return dict(app=app, db=db, models=models)
manager.add_command("shell", Shell(make_context=make_context, use_ipython=True))
manager.add_command('db', MigrateCommand)


@manager.command
def create_admin():
    # create admin role if not exists
    admin_role = models.Role.query.filter_by(name="admin").first()
    if admin_role is None:
        admin_role = models.Role(name="admin", description="Admin")

    user = models.User(
        email="ad@min.com",
        password=models.User.hashed_password("admin"),
        active=True,
        confirmed=True,
        registered_on=datetime.datetime.now(),
        confirmed_at=datetime.datetime.now())

    user.roles.append(admin_role)
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
