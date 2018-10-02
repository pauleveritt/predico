from predico.sample import servicemanager, setup

if __name__ == '__main__':
    setup()
    output = servicemanager.render('more/index')
    print(output)
