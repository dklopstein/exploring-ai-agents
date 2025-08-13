from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 

        sigma = {'conflict': False} # assignment function
        delta = [] # decision stack

        while True:
            sigma, domains = self.propagate(sigma, domains)
            if not sigma['conflict']:
                if len(sigma) - 1 == len(sd_spots):
                    for spot in sd_spots:
                        domains[spot] = [sigma[spot]]
                    return domains
                else:
                    sigma, cell = self.make_decision(sigma, domains)
                    delta.append((copy.deepcopy(sigma), cell, copy.deepcopy(domains)))

            else:
                # decision stack is empty; there is no solution
                if not delta: 
                    return None 
                else:
                    sigma, domains = self.backtrack(delta)
        
    def arc_consistent(self, cell, value, sigma, domains):
        for peer in sd_peers[cell]:
            if peer in sigma and sigma[peer] == value:
                return False
            elif peer not in sigma and len(domains[peer]) == 1 and domains[peer][0] == value:
                return False
            
        return True

    def propagate(self, sigma, domains):
        while True:
            changed = False
            for cell in sd_spots:
                if cell not in sigma and len(domains[cell]) == 1:
                    sigma[cell] = domains[cell][0]
                    changed = True
        
                if cell in sigma and len(domains[cell]) > 1:
                    domains[cell] = [sigma[cell]]
                    changed = True

                if not domains[cell]:
                    sigma["conflict"] = True
                    return sigma, domains
                
                # check arc consistency
                if cell not in sigma:
                    new_domain = []
                    for value in domains[cell]:
                        if self.arc_consistent(cell, value, sigma, domains):
                            new_domain.append(value)
                    
                    if len(new_domain) < len(domains[cell]):
                        changed = True
                    
                    domains[cell] = new_domain

            if not changed:
                return sigma, domains

    
    def make_decision(self, sigma, domains):
        unassigned_cells = [(cell, len(domains[cell])) for cell in domains \
                            if cell not in sigma and len(domains[cell]) > 0]
        unassigned_cells.sort(key=lambda x: x[1]) # sort by shortest domain
        cell = unassigned_cells[0][0]
        value = domains[cell][0] # get first value of shortest domain
        sigma[cell] = value # update assigned value

        return sigma, cell
    
    def backtrack(self, delta):
        sigma, cell, domains = delta.pop()
        sigma['conflict'] = False
        value = sigma[cell]
        sigma.pop(cell)
        domains[cell].remove(value)

        return sigma, domains

    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
