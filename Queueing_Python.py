#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
# https://towardsdatascience.com/simulating-a-queuing-system-in-python-8a7d1151d485 used this as reference for queuing in Python


class Passenger:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.service_end_time = None
        self.waiting_time = None

class ServiceStation:
    def __init__(self):
        self.busy = False
        self.current_passenger = None
        self.total_service_time = 0

class Queue:
    def __init__(self, num_service_stations, arrival_rate, service_rate, sim_time, policy):
        self.num_service_stations = num_service_stations
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.sim_time = sim_time
        self.policy = policy

        self.current_time = 0
        self.passenger_queues = []
        
        for i in range(num_service_stations):
          self.passenger_queues.append([])
        
        self.service_stations = []  
        for i in range(num_service_stations):
          self.service_stations.append(ServiceStation())
        self.stats = {'max_queue_length': 0, 'total_waiting_time': 0, 'max_waiting_time': 0,
                      'num_passengers': 0, 'total_service_time': 0}

    def choose_queue(self):
        if self.policy == 'round_robin': #2A
            queue_id = self.current_time % self.num_service_stations
        elif self.policy == 'single': #option1
          queue_id = 0  #always use the first queue
        elif self.policy == 'shortest': #2B
        
          min_length = len(self.passenger_queues[0])
          queue_id = 0
          for i in range(self.num_service_stations):
            for j in range(i+1, self.num_service_stations):
              if len(self.passenger_queues[j]) < len(self.passenger_queues[i]):
                min_length = len(self.passenger_queues[j])
                queue_id = j
            if len(self.passenger_queues[i]) < min_length:
              min_length = len(self.passenger_queues[i])
              queue_id = i

          
            
        elif self.policy == 'random': #2C
            queue_id = random.randint(0, self.num_service_stations-1)
        return queue_id

    def run(self):
        while self.current_time < self.sim_time:
            # generate new passenger arrivals
            if self.current_time < self.sim_time:
                if random.random() < self.arrival_rate:
                    queue_id = self.choose_queue()
                    self.passenger_queues[queue_id].append(Passenger(self.current_time))
            # service start event
            for ss_id, ss in enumerate(self.service_stations):
                if not ss.busy:
                  if self.passenger_queues[ss_id]:
                    passenger = self.passenger_queues[ss_id].pop(0)
                    passenger.service_start_time = self.current_time
                    ss.current_passenger = passenger
                    ss.busy = True
            # service end event
            for ss_id, ss in enumerate(self.service_stations):
                if ss.busy:
                    passenger = ss.current_passenger
                    if self.current_time - passenger.service_start_time >= self.service_rate:
                        passenger.service_end_time = self.current_time
                        ss.busy = False
                        ss.total_service_time += self.current_time - passenger.service_start_time
                        self.stats['total_service_time'] += self.current_time - passenger.service_start_time
                        self.stats['total_waiting_time'] += passenger.service_start_time - passenger.arrival_time
                        self.stats['num_passengers'] += 1
                        self.stats['max_waiting_time'] = max(self.stats['max_waiting_time'], passenger.service_start_time - passenger.arrival_time)
                        ss.current_passenger = None
            # update statistics
            max_queue_length = 0
            for q in self.passenger_queues:
              queue_length = 0
              for passenger in q:
                queue_length += 1
                if queue_length > max_queue_length:
                  max_queue_length = queue_length
            self.stats['max_queue_length'] = max(self.stats['max_queue_length'], max_queue_length)
            # move time forward
            self.current_time += 1

        self.stats['avg_waiting_time'] = round(self.stats['total_waiting_time'] / self.stats['num_passengers'],2)
        self.stats['avg_service_time'] = round(self.stats['total_service_time'] / self.stats['num_passengers'],2)
        for i, ss in enumerate(self.service_stations):
            print(f'Station {i+1} occupancy rate: {round((ss.total_service_time/self.sim_time)*100,2)}%')
        return self.stats

num_service_stations = 3
arrival_rate = 1/2 # average interarrival time is 2 minutes
service_rate = 10 # average service time is 10 minutes
sim_time = 10000
policies = ['single', 'round_robin', 'shortest', 'random']

q = Queue(num_service_stations, arrival_rate, service_rate, sim_time, 'round_robin')
s = q.run()      
print(s)


# In[2]:


q = Queue(num_service_stations, arrival_rate, service_rate, sim_time, policies[3] )


s = q.run()
print(s)


# In[ ]:




