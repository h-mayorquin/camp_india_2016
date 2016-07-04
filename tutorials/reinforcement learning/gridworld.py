import operator
import random
import matplotlib.pyplot as pl
"""
code adapted from http://aima.cs.berkeley.edu/python/mdp.html
"""

class MDP:
    """A Markov Decision Process, defined by an initial state, transition model,
    and reward function. We also keep track of a gamma value, for use by
    algorithms. The transition model is represented somewhat differently from
    the text.  Instead of P(s|a, s') being  probability number for each
    state/action/state triplet, we instead have T(s, a) return a list of (p, s')
    pairs.  We also keep track of the possible states, terminal states, and
    actions for each state."""

    def __init__(self, init, actlist, terminals, gamma=.9):
        update(self, init=init, actlist=actlist, terminals=terminals,
               gamma=gamma, states=set(), reward={})

    def R(self, state):
        "Return a numeric reward for this state."
        return self.reward[state]

    def T(state, action):
        """Transition model.  From a state and an action, return a list
        of (result-state, probability) pairs."""
        abstract

    def actions(self, state):
        """Set of actions that can be performed in this state.  By default, a
        fixed list of actions, except for terminal states. Override this
        method if you need to specialize by state."""
        if state in self.terminals:
            return [None]
        else:
            return self.actlist

class GridMDP(MDP):
    """A two-dimensional grid MDP.  All you have to do is
    specify the grid as a list of lists of rewards; use None for an obstacle
    (unreachable state).  Also, you should specify the terminal states.
    An action is an (x, y) unit vector; e.g. (1, 0) means move east."""
    def __init__(self, grid, terminals, init=(0, 0), gamma=.9):
        grid.reverse() ## because we want row 0 on bottom, not on top
        MDP.__init__(self, init, actlist=orientations,
                     terminals=terminals, gamma=gamma)
        update(self, grid=grid, rows=len(grid), cols=len(grid[0]))
        for x in range(self.cols):
            for y in range(self.rows):
                self.reward[x, y] = grid[y][x]
                if grid[y][x] is not None:
                    self.states.add((x, y))

    def T(self, state, action):
        if action == None:
            return [(0.0, state)]
        else:
            return [(0.8, self.go(state, action)),
                    (0.1, self.go(state, turn_right(action))),
                    (0.1, self.go(state, turn_left(action)))]

    def go(self, state, direction):
        "Return the state that results from going in this direction."
        state1 = vector_add(state, direction)
        return if_(state1 in self.states, state1, state)

    def to_grid(self, mapping):
        """Convert a mapping from (x, y) to v into a [[..., v, ...]] grid."""
        return list(reversed([[mapping.get((x,y), None)
                               for x in range(self.cols)]
                              for y in range(self.rows)]))

    def to_arrows(self, policy):
        chars = {(1, 0):'>', (0, 1):'^', (-1, 0):'<', (0, -1):'v', None: '.'}
        return self.to_grid(dict([(s, chars[a]) for (s, a) in policy.items()]))


    def new_state(self, state, action):
	""" Returns the new state, when action is selected in state """
	random_draw = random.uniform(0,1)
	if random_draw < self.T(state,action)[0][0]:
		return self.T(state,action)[0][1]
	elif random_draw < self.T(state,action)[0][0]+self.T(state,action)[1][0]:
		return self.T(state,action)[1][1]
	else:
		return self.T(state,action)[2][1]	

    def policy_plot(self, pi):
	""" Plots the policy on the grid """
	ax=pl.axes()
	col = max([s[0] for s in self.states])+1	
	rows = max([s[1] for s in self.states])+1
	for s in self.states:
		    try:
		        ax.arrow(s[0]+0.5-0.3*pi[s][0],s[1]+0.5-0.3*pi[s][1], 0.6*pi[s][0], 0.6*pi[s][1], head_width=0.05, head_length=0.1, fc='k', ec='k')
		    except:
			pass
	ax.set_xlim([0,col])
	ax.set_ylim([0,rows])
	ax.set_xticks(range(col))
	ax.set_yticks(range(rows))
	ax.set_xticklabels([])
	ax.set_yticklabels([])
	pl.grid()
	pl.show()
	return

    def v_plot(self,V):
	"""" Returns a plot of the value function """
	col = max([s[0] for s in self.states])+1	
	rows = max([s[1] for s in self.states])+1
	ax=pl.axes()
	colorlerp = lambda a, b, t: map(lambda x,y: x+(y-x)*t*t, a, b)
	green = [0.,.8,0.]
	red = [.8,0.,0.]	
	for s in self.states:
		pl.fill_between([s[0],s[0]+1],[s[1],s[1]],s[1]-1,color=colorlerp(red, green, (V[s]+1)/2.))
		ax.text(s[0]+0.1,s[1]-0.9,str(V[s])[0:6])
	ax.set_xticks(range(col))
	ax.set_yticks(range(rows))
	ax.set_xticklabels([])
	ax.set_yticklabels([])
	pl.grid()
	pl.show()
	return

    def q_plot(self,Q):
	"""" Returns a plot of the q-function """
	col = max([s[0] for s in self.states])+1	
	rows = max([s[1] for s in self.states])+1
	ax=pl.axes()
	colorlerp = lambda a, b, t: map(lambda x,y: x+(y-x)*t*t, a, b)
	green = [0.,.8,0.]
	red = [.8,0.,0.]	
	for s in self.states:
		for a in self.actions(s):
			try:
				pl.fill_between([s[0]+max(a[0],0),s[0]+0.5,s[0]+1+min(a[0],0)],[s[1]+min(1+a[1],1)]*3,[s[1]+max(a[1],0), s[1]+0.5, s[1]+abs(a[0])+max(a[1],0)],color=colorlerp(red, green, (Q[s,a]+1)/2.))
				ax.text(s[0]+0.3+0.25*a[0],s[1]+0.45+0.4*a[1],str(Q[s,a])[0:6])
			except:
				if s in self.terminals:
				    pl.fill_between([s[0],s[0]+1],[s[1]+1,s[1]+1],s[1],color=colorlerp(red, green, (Q[s,None]+1)/2.))
				    ax.text(s[0]+0.3,s[1]+0.45,str(Q[s,None])[0:6])
				pass
	ax.set_xticks(range(col))
	ax.set_yticks(range(rows))
	ax.set_xticklabels([])
	ax.set_yticklabels([])
	pl.grid()
	pl.show()
	return
				
	

def update(x, **entries):
    """Update a dict; or an object with slots; according to entries.
    >>> update({'a': 1}, a=10, b=20)
    {'a': 10, 'b': 20}
    >>> update(Struct(a=1), a=10, b=20)
    Struct(a=10, b=20)
    """
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x


# orienation tuples allowed: (1,0): move east; (-1,0): west; (0,1): up;  (0,-1): down
orientations = [(1,0), (0, 1), (-1, 0), (0, -1)]
def turn_right(orientation):
    return orientations[orientations.index(orientation)-1]

def turn_left(orientation):
    return orientations[(orientations.index(orientation)+1) % len(orientations)]


def vector_add(a, b):
    """Component-wise addition of two vectors.
    >>> vector_add((0, 1), (8, 9))
    (8, 10)
    """
    return tuple(map(operator.add, a, b))

def if_(test, result, alternative):
    """Like C++ and Java's (test ? result : alternative), except
    both result and alternative are always evaluated. However, if
    either evaluates to a function, it is applied to the empty arglist,
    so you can delay execution by putting it in a lambda.
    >>> if_(2 + 2 == 4, 'ok', lambda: expensive_computation())
    'ok'
    """
    if test:
        if callable(result): return result()
        return result
    else:
        if callable(alternative): return alternative()
        return alternative
