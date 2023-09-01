import numpy as np

def check_solution(states,edges,n,count):
    """    
    Check solution for errors
    """  
    childedgelist = []
    for i in range(n):
        childedgelist.append([])
    
    for child,father in edges:
        childedgelist[child].append(father)
        
    
    # check validity of solution
    for time in range(count):
        for vertex in range(n):
            if (states[time][vertex] == 0 and states[time+1][vertex] == 1) or (states[time][vertex] == 1 and states[time+1][vertex] == 0) or (states[time][vertex] == 2 and states[time+1][vertex] == 1): # vertex pebbled or unpebbled or unspooked
                for child in childedgelist[vertex]:
                    if states[time][child] != 1 or states[time+1][child] != 1:
                        print("ERROR: the optimized solution is not valid, child not pebbled", vertex,child,time)
                        print(states[time][vertex],states[time+1][vertex])
        if (states[time][vertex] == 2 and states[time+1][vertex] == 0):
            print("ERROR: the optimized solution is not valid, vertex unpebbled without spook",vertex,time)
        if (states[time][vertex] == 0 and states[time+1][vertex] == 2):
            print("WARNING: optimized solution has strange but valid behavior",vertex,time)
    return
    

def remove_useless_pebbling(states,n,edgelist,count):
    """
    Optimize the sequential pebbling time of solution. 
    Pebbles that are not used to (un)pebble or unspook a succesor are detected and removed.
    
    Output: optimized solution in the form of a state matrix
    """
    for time in range(count,0,-1):
        for vertex in range(n):
            if states[time][vertex] == 0 and states[time-1][vertex] == 1:
                father_pebbled = False
            
                t = time
                while not(father_pebbled):
                    
                    if states[t][vertex] == 2: # if pebble was placed to unspook
                        break
                    
                    if states[t][vertex] == 0 and time != t and not(father_pebbled): # at this timestep the vertex was pebbled
                    #print()
                        for i in range(t,time,1): # remove the pebbles at the timestep
                            states[i][vertex] = 0
                        break
                    
                    for father in edgelist[vertex]: #check if a father is pebbled/unpebbled or unspooked during pebbling of vertex
                        if (states[t][father] == 0 and states[t-1][father] == 1) or (states[t][father] == 1 and states[t-1][father] == 0) or (states[t][father] == 1 and states[t-1][father] == 2):
                            father_pebbled = True
                            break
                        #print(vertex)

                    t-=1 # go to previous timestep
                
    return states
    
def replace_spook_by_pebble_asap(states,n,edgelist,max_pebbles,count):
    """
    Optimize the sequential pebbling time of solution. 
    Remove spooks as soon as their inputs are pebbled and there is a pebble available.
    
    FUNCTION IS UNDER CONSTRUCTION...
    
    Output: optimized solution in the form of a state matrix
    """
    pebbles_used = n-np.count_nonzero(states-1, axis = 1)
    return states
    
def delay_spook_placement(states,n,max_pebbles,count):
    """
    Optimize the sequential pebbling time of solution. 
    Delay the spook placements if enough pebbles are available. 
    
    Output: optimized solution in the form of a state matrix
    """
    pebbles_used = n-np.count_nonzero(states-1, axis = 1)
    
    for time in range(1,count+1,1):
        if pebbles_used[time] < max_pebbles: # maximal number of pebbles not reached
            
            #delayable_vertixes = []
            for vertex in range(n):
                if states[time][vertex] == 2 and states[time-1][vertex] == 1:  # spooking move
                    #delayable_vertices.append(vertex)
                    #print("delayed at time",time)                    
                    states[time][vertex] = 1
                    pebbles_used[time] += 1
                    
                    
                    if pebbles_used[time] >= max_pebbles:
                        break
                    
            #for vertex in delayable_vertices:
            #    states[time][vertex] = 1
    return states
    
    
def remove_useless_spookings(states,n,inv_edgelist,count):
    """
    Optimize the sequential pebbling time of solution. 
    Spookings moves with all inputs pebbled are changed into unpebbling moves. 
    
    Output: optimized solution in the form of a state matrix
    """
    for time in range(count,0,-1):
        for vertex in range(n):
            if states[time][vertex] == 2 and states[time-1][vertex] == 1:  # spooking move
            
                useless_spooking = True
                for child in inv_edgelist[vertex]: # check if inputs of vertex were pebbled at time
                    if not(states[time][child] == 1 and states[time-1][child] == 1):
                        useless_spooking = False
                        break
                
                if useless_spooking:
                    #print("unspooked")
                    # remove spook
                    t=time
                    while(states[t][vertex] == 2):
                        states[t][vertex] = 0
                        t += 1
                    
    return states

def par2seq(states,n,count):
    """
    Convert parrallel solution to sequential pebbling solution.
    
    Output: sequential pebbling solution [np array] and number of sequential moves 
    """
    
    seqStates = []
    seqCount = count
    
    states = states.tolist()
    
    seqStates.append(states[0])
    
    for time in range(0,count):
        pebbling = []
        unpebbling = []
        spooking = []
        unspooking = []
        
        for vertex in range(n):
            if states[time][vertex] != states[time+1][vertex]:
                start = states[time][vertex]
                next = states[time+1][vertex]
                if start == 0 and next == 1:
                    pebbling.append(vertex)
                elif start == 1 and next == 0:
                    unpebbling.append(vertex)
                elif start == 1 and next == 2:
                    spooking.append(vertex)
                elif start == 2 and next == 1:
                    unspooking.append(vertex)
                    
        for vertex in unpebbling:
            newState = list(seqStates[-1])
            newState[vertex] = 0
            seqStates.append(newState)
        """
        for vertex in unspooking:
            newState = list(seqStates[-1])
            newState[vertex] = 1
            seqStates.append(newState)
            
        for vertex in spooking:
            newState = list(seqStates[-1])
            newState[vertex] = 2
            seqStates.append(newState)
        """
        while(len(unspooking)>0 or len(spooking)>0):
            if len(unspooking)>0:
                vertex = unspooking.pop(0)
                newState = list(seqStates[-1])
                newState[vertex] = 1
                seqStates.append(newState)
            
            if len(spooking)>0:
                vertex = spooking.pop(0)
                newState = list(seqStates[-1])
                newState[vertex] = 2
                seqStates.append(newState)
        
        for vertex in pebbling:
            newState = list(seqStates[-1])
            newState[vertex] = 1
            seqStates.append(newState)
    
    seqCount = len(seqStates)-1
    seqStates = np.array(seqStates)
    print(seqStates)
    return (seqStates,seqCount)
    
def optimize_states(states,n,(edgelist,inv_edgelist),(max_pebbles,max_spooks),count):
    """
    Optimize the sequential pebbling time of solution. 
    Useless pebblings/unpebblings/spookings/unspookings are detected and removed.
    
    Output: optimized solution in the form of a state matrix
    """
    
    (states,count) = par2seq(states,n,count)
    states = remove_useless_spookings(states,n,inv_edgelist,count)
    
    states = remove_useless_pebbling(states,n,edgelist,count)
    states = delay_spook_placement(states,n,max_pebbles,count)
    
    return (states, count)
