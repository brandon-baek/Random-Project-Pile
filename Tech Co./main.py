from difflib import get_close_matches as gcm
from os import system as sys
from names import get_full_name
from random import choice, randint, shuffle

PROJECT_TYPES = ['App', 'Device', 'OS', 'AI/ML']


def move_on():
    input('\nEnter anything to move on ')
    sys('clear')


class Employee:
    def __init__(self):
        self.name = get_full_name()
        self.age = randint(18, 80)
        self.project = ''
        self.skillset = {
            'software': randint(0, 100),
            'hardware': randint(0, 100),
            'ai/ml': randint(0, 100),
            'design': randint(0, 100)
        }
        self.position = max(self.skillset, key=self.skillset.get)
        self.pay = sum(self.skillset.values()) * 50
        self.happiness = 100

    def age_one_year(self):
        self.age += 1

    def research(self, topic, points):
        if topic == self.position:
            self.skillset[topic] += points / (self.age / 10)

    def beneficial(self):
        return self.pay / self.skillset[self.position] > 1000

    def raise_decision(self, decision):
        if decision:
            if self.beneficial():
                self.happiness += 10
            else:
                self.happiness += 5
        else:
            if self.beneficial():
                self.happiness -= 10
            else:
                self.happiness -= 5

    def print_details(self):
        print(f'Name: {self.name}\n'
              f'Age: {self.age}\n'
              f'Pay: ${self.pay}/month\n'
              f'Position: {self.position}\n\n'
              f'Skillsets:\n'
              f'Software: {self.skillset['software']}\n'
              f'Hardware: {self.skillset['hardware']}\n'
              f'Design: {self.skillset['design']}\n'
              f'AI/ML: {self.skillset['ai/ml']}\n')


class Project:
    def __init__(self, project_name, project_type, workers, month):
        self.project_name = project_name
        self.project_type = project_type
        self.project_workers = workers
        self.finished_state = False
        self.published = False
        self.project_needs = []
        self.project_quality_score = 0
        match self.project_type:
            case 'ai/ml':
                self.project_needs = ['ai/ml', 'software']
                self.project_finish_time = month + 15
            case 'os':
                self.project_needs = ['software', 'design']
                self.project_finish_time = month + 10
            case 'device':
                self.project_needs = ['software', 'hardware', 'design']
                self.project_finish_time = month + 5
            case 'app':
                self.project_needs = ['software', 'design']
                self.project_finish_time = month + 1
            case _:
                self.project_needs = None
                self.project_finish_time = None

    def determine_quality(self):
        score = 0
        for need in self.project_workers:
            for worker in self.project_workers[need]:
                score += worker.skillset[need]
        self.project_quality_score = score / 10

    def publish(self):
        self.published = True

    def sales(self, company):
        if self.published:
            money_made = self.project_quality_score * 10000
            company.value += money_made
            self.project_quality_score -= 10
            return money_made


class Company:
    def __init__(self, name):
        self.name = name
        self.value = 0
        self.projects = []
        self.employees = []
        self.available_employees = []

    def reload_available_employees(self):
        self.available_employees = []
        for employee in self.employees:
            if not employee.project:
                self.available_employees.append(employee)


user = Company(input('Name of Company: '))
month = 1
emails = []
resume_max = 8
discontinued_history = []
bad_events = {
    'We just got sued, it\'s gonna cost a bit of money... $5000 to be exact...': 5000,
    'Our Office building had a leak after the rainstorm, it\'s gonna cost $2000': 2000,
    'Our Office got robbed, $3000 was stolen...': 3000,
    'We had an earthquake, repair costs are about $1000': 1000,
    'Someone copied our Idea, we need to sue! It\'s gonna cost $3000.': 3000
}


def develop():
    if len(user.available_employees) >= 2:
        project_name = input('Name of project: ')
        sys('clear')
        for order, pro_type in enumerate(PROJECT_TYPES, start=1):
            print(f'{order}. {pro_type}')
        project_type = PROJECT_TYPES[int(input('Type of project: ')) - 1].lower()
        sys('clear')
        project_needs = Project('temp', project_type, None, month).project_needs
        if len(project_needs) > len(user.available_employees):
            print('You don\'t have enough workers!')
            move_on()
            return None
        project_workers = {}
        for need in project_needs:
            project_workers[need] = []
        while True:
            sys('clear')
            for need in project_workers:
                project_workers_string = ''
                for worker in project_workers[need]:
                    if project_workers_string:
                        project_workers_string += ', ' + worker.name
                    else:
                        project_workers_string += worker.name
                print(f'{need}: {project_workers_string}')
            print('\nYour Available Employees:')
            employee_names = ['exit']
            for employee in user.employees:
                if not employee.project:
                    employee_names.append(employee.name)
                    print(employee.name)
            user_choice_employee = gcm(input('\nWho would you like to add? (Enter "exit" to finish): '),
                                       employee_names,
                                       1,
                                       0)[0]
            if user_choice_employee != 'exit':
                user_choice_sector = gcm(input('Where do you want to put this employee?: '),
                                         project_needs,
                                         1,
                                         0)[0]
                for employee in user.employees:
                    if employee.name == user_choice_employee:
                        user_choice_employee = employee
                        employee.project = project_name
                        user.reload_available_employees()
                project_workers[user_choice_sector].append(user_choice_employee)
            else:
                leaving_empty = False
                for workers in project_workers.values():
                    if not workers:
                        leaving_empty = True
                        break
                if leaving_empty:
                    print('You are exiting without finishing project setup, are you sure?')
                    if input('(y/n)').lower() == 'y':
                        return None
                else:
                    user.projects.append(Project(project_name, project_type, project_workers, month))
                    return None
    else:
        print('You don\'t have enough employees!')
        move_on()


def research():
    if len(user.employees) >= 1:
        print('Which skill would you like to research?\n1. Software\n2. Design\n3. Hardware\n4. AI/ML')
        user_choice = 0
        while 1 > user_choice < 4:
            try:
                user_choice = int(input(''))
            except:
                pass
        sys('clear')

        user_budget = int(input('Your budget?\n')) / 100
        sys('clear')

        if user_choice == 1:
            user_choice = 'software'
        elif user_choice == 2:
            user_choice = 'design'
        elif user_choice == 3:
            user_choice = 'hardware'
        else:
            user_choice = 'ai/ml'

        for employee in user.employees:
            employee.research(user_choice, user_budget)
        print('Research Complete.')
        move_on()
    else:
        print('You don\'t have enough employees!')
        move_on()


def check_email():
    if emails:
        print('[INBOX]\n')
        for email in emails:
            print(email)
        move_on()
    else:
        print('Empty Inbox')
        move_on()


def hire():
    global resume_max
    if resume_max > 0:
        possible_employee = Employee()
        possible_employee.print_details()
        print('(1) Hire | (2) Reject')
        try:
            if int(input('')) == 1:
                sys('clear')
                user.employees.append(possible_employee)
                user.reload_available_employees()
                print(f'{possible_employee.name} is hired!')
            else:
                sys('clear')
                print(f'{possible_employee.name} is rejected...')
        except:
            sys('clear')
            print(f'{possible_employee.name} is rejected...')
        move_on()
        resume_max -= 1
    else:
        print('No one is looking for a job...')
        move_on()


def manage_projects():
    if user.projects:
        print(f'{user.name} Projects:\n')
        for order, project in enumerate(user.projects, start=1):
            print(f'{order} | {project.project_name} {project.project_type} ', end='')
            if not project.finished_state:
                print('Not finished')
            else:
                print('Finished')
        while True:
            try:
                user_choice = input('\nWhich project would you like to manage? (Enter "exit" to leave)\n')
                if (1 <= int(user_choice) <= len(user.projects)) or user_choice.lower() == 'exit':
                    break
            except:
                pass
        if user_choice != 'exit':
            sys('clear')
            user_project_choice = user.projects[int(user_choice) - 1]
            print(user_project_choice.project_name, '\n')
            print('Type:', user_project_choice.project_type)
            print('Finished?', user_project_choice.finished_state)
            print('Published?', user_project_choice.published)
            print('Workers:')
            for need in user_project_choice.project_workers:
                worker_list_string = ''
                for worker in user_project_choice.project_workers[need]:
                    if worker_list_string:
                        worker_list_string += ', ' + worker.name
                    else:
                        worker_list_string += worker.name
                print(f'  |   {need}: {worker_list_string}')
            if not user_project_choice.finished_state:
                print(f'\nFinishes in month {user_project_choice.project_finish_time}')
            else:
                print(f'Quality Score: {user_project_choice.project_quality_score}')
            while True:
                try:
                    user_choice = int(input('Options: (1) Publish | (2) Discontinue Project | (3) Exit\n'))
                    if user_choice in [1, 2, 3]:
                        break
                except:
                    pass
            sys('clear')
            match user_choice:
                case 1:
                    if user_project_choice.finished_state:
                        user_project_choice.publish()
                        print(f'Project "{user_project_choice.project_name}" has been published')
                    else:
                        print('This project is not yet finished')
                case 2:
                    discontinued_history.append(user_project_choice)
                    user.projects.remove(user_project_choice)
                    print(f'Project "{user_project_choice.project_name}" has been discontinued')
                case 3:
                    return None
            move_on()
    else:
        print('You have no projects...')
        move_on()


def manage_employees():
    for order, employee in enumerate(user.employees, start=1):
        print(f'{order}. {employee.name}')
    while True:
        user_choice = input('Which Employee would you like to edit? (Enter "exit" to leave)\n')
        try:
            if 1 <= int(user_choice) <= len(user.employees):
                break
        except:
            if user_choice.lower() == 'exit':
                break
        user_choice = input('Which Employee would you like to edit? (Enter "exit" to leave)\n')
    sys('clear')
    if user_choice.lower() != 'exit':
        user_employee_choice = user.employees[int(user_choice) - 1]
        user_employee_choice.print_details()
        print('Currently Working on:', user_employee_choice.project)
        print('Happiness:', user_employee_choice.happiness)
        while True:
            try:
                user_choice = int(input('\n(1) Raise Pay | (2) Cut Pay | (3) Fire | (4) Exit\n'))
                if 1 <= user_choice <= 4:
                    break
            except:
                pass
        sys('clear')
        match user_choice:
            case 1:
                pay_raise = int(input('How much would you like to raise pay?\n'))
                sys('clear')
                user_employee_choice.pay += pay_raise
                user_employee_choice.happiness += pay_raise % 100
                print(f'{user_employee_choice.name} thanks you for the raise, they are now happier')
            case 2:
                pay_cut = int(input('How much would you like to cut pay?\n'))
                sys('clear')
                user_employee_choice.pay -= pay_cut
                user_employee_choice.happiness -= pay_cut % 100
                print(f'{user_employee_choice.name} hates you for the cut, they are now sadder')
            case 3:
                print(f'{user_employee_choice.name} has been fired')
                user.employees.remove(user_employee_choice)
                user.reload_available_employees()
            case _:
                return None
        move_on()


def sleep():
    global emails
    global resume_max
    global month
    month += 1
    emails = []
    resume_max = randint(5, 10)
    if month % 12 == 0:
        for employee in user.employees:
            employee.age_one_year()
    total_sales = 0
    for project in user.projects:
        if project.project_finish_time == month:
            project.finished_state = True
            for worker in project.project_workers:
                worker.project = ''
        if project.published:
            sales = project.sales(user)
            total_sales += sales
            if sales > 0:
                emails.append(f'Sales Department: We made ${sales:,} from {project.project_name}.')
            elif sales < 0:
                emails.append(f'Sales Department: We just lost ${sales:,} from {project.project_name}.')
            else:
                emails.append(
                    f'Sales Department: We have made no money nor have we lost any money from {project.project_name}.')

    employee_pay = 0
    for employee in user.employees:
        employee_pay += employee.pay
    project_maintain_cost = len(user.projects) * 100
    income_tax = total_sales * 0.08

    if income_tax:
        user.value -= income_tax
        emails.append(f'IRS: A Deduction of ${income_tax:,} from your total sales has been made. That is 8%.')
    if project_maintain_cost:
        user.value -= project_maintain_cost
        emails.append(f'PMO: Maintaining Projects and Licenses have costed ${project_maintain_cost:,}')
    if employee_pay:
        user.value -= employee_pay
        emails.append(f'HR: Employee Salaries have costed ${employee_pay:,}')

    for _ in range(10):
        if randint(1, 20) == 1:
            bad_event = choice(list(bad_events))
            email_for_bad_event = ''
            email_for_bad_event += choice(user.employees).name + ': '
            email_for_bad_event += bad_event
            user.value -= bad_events[bad_event]

    shuffle(emails)
    user.reload_available_employees()


def main():
    while True:
        sys('clear')
        print(f'{user.name}\n')
        print('Month:', month)
        print('Value:', user.value)
        print()
        print('1. Develop\n'
              '2. Research\n'
              f'3. Check Email ({len(emails)})\n'
              '4. Hire Employees\n'
              '5. Manage Projects\n'
              '6. Manage Employees\n'
              '7. Sleep\n\n')
        try:
            user_choice = int(input('What would you like to do? '))
        except:
            user_choice = None
        sys('clear')
        match user_choice:
            case 1:
                develop()
            case 2:
                research()
            case 3:
                check_email()
            case 4:
                hire()
            case 5:
                manage_projects()
            case 6:
                manage_employees()
            case 7:
                sleep()


if __name__ == '__main__':
    main()
