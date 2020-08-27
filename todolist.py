from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


Base = declarative_base(())


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Nothing to do!')
    deadline = Column(Date, default=datetime.today())

    def __repr___(self):
        return self.task


def print_todays_task():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()

    if session.query(Table).first() is None:
        print('Today {} {}:'.format(datetime.today().strftime('%-d'), datetime.today().strftime('%b')))
        print('Nothing to do!')
        print()
    else:
        print('Today {} {}:'.format(datetime.today().strftime('%-d'), datetime.today().strftime('%b')))
        i = 1
        for row in rows:
            print("{}. {}".format(i, row.task))
            i += 1
        print('')


# # adding new row to the table
def add_task():
    task_description = input('Enter task:\n')
    deadline_date = input('Enter deadline:\n')
    datetime_obj_with_deadline_date = datetime.strptime(deadline_date, '%Y-%m-%d')
    new_row = Table(task=task_description, deadline=datetime_obj_with_deadline_date)
    session.add(new_row)
    session.commit()
    print('The task has been added!')


def print_weeks_tasks():
    for day in [datetime.today() + timedelta(days=i) for i in range(7)]:

        rows = session.query(Table).filter(Table.deadline == day.strftime('%Y-%m-%d')).\
            order_by(Table.deadline).all()
        print('{} {}:'.format(day.strftime('%A'), day.strftime('%-d %b')))
        if rows:
            for n, task in enumerate(rows, 1):
                print('{}. {}'.format(n, task.task))
                print('')
        else:
            print('Nothing to do!')
            print('')
    print('')


def print_all_tasks():
    print('All tasks:')
    all_tasks = session.query(Table).order_by(Table.deadline).all()
    i = 1
    for row in all_tasks:

        print('{}. {}. {}'.format(i, row.task, row.deadline.strftime('%-d %b')))
        i += 1
    print()


def print_missed_tasks():
    print('Missed tasks:')

    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()

    if rows:
        count = 1
        for row in rows:
            print('{}. {}. {}'.format(count, row.task, row.deadline.strftime('%-d %b')))
            count += 1
    else:
        print('Nothing is missed!')
    print('')


def delete_task():

    rows = session.query(Table).order_by(Table.deadline).all()
    if rows:
        print('Choose the number of the task you want to delete:')
        count = 1
        for row in rows:
            print('{}. {}. {}'.format(count, row.task, row.deadline.strftime('%-d %b')))
            count += 1

        task_to_delete = int(input()) - 1
        row_to_delete = rows[task_to_delete]
        session.delete(row_to_delete)
        session.commit()
        print('The task has been deleted!')
        print('')


# creating a model table
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def main():
    while True:
        print('1) Today\'s tasks')
        print('2) Week\'s tasks')
        print('3) All tasks')
        print('4) Missed tasks')
        print('5) Add task')
        print('6) Delete task')
        print('0) Exit')
        a = input()
        if a == '1':
            print()
            print_todays_task()
        elif a == '2':
            print('')
            print_weeks_tasks()
        elif a == '3':
            print('')
            print_all_tasks()
        elif a == '4':
            print('')
            print_missed_tasks()
        elif a == '5':
            print('')
            add_task()
            print()
        elif a == '6':
            print('')
            delete_task()
        elif a == '0':
            print()
            print('Bye!')
            break


main()
session.close()
