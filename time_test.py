import Meanders_Beta.all_functions as mbaf


iterations = 5
for n in range(2, 20, 2):
    local_time = 0
    for i in range(iterations):
        local_meanders = mbaf.Meanders(n)
        local_meanders.get_all_meanders()
        local_time += local_meanders.speed
        print(i, local_meanders.speed)
    print(f"Для меандров размера {n} среднее время работы составляет {local_time / iterations}")
    print()
