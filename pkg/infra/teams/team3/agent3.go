package team3

import (
	"infra/config"
	"infra/game/agent"
	"infra/game/commons"
	"infra/game/decision"
	"infra/logging"
	"math/rand"
	"os"
	"strconv"

	"github.com/benbjohnson/immutable"
)

type AgentThree struct {
	AT                    int
	SH                    int
	uR                    map[commons.ID]int
	uP                    map[commons.ID]int
	uC                    map[commons.ID]int
	utilityScore          map[commons.ID]int
	TSN                   []commons.ID
	contactsLastRound     map[commons.ID]bool
	chairTolerance        int
	proposalTolerance     map[commons.ID]int
	fightDecisionsHistory commons.ImmutableList[decision.ImmutableFightResult]
	personality           int
	sanctioned            int
	statsQueue            StatsQueue
}

// Update internal parameters at the end of each stage
func (a *AgentThree) UpdateInternalState(baseAgent agent.BaseAgent, _ *commons.ImmutableList[decision.ImmutableFightResult], votes *immutable.Map[decision.Intent, uint], log chan<- logging.AgentLog) {
	AS := baseAgent.AgentState()
	view := baseAgent.View()
	// Initialise utils
	if view.CurrentLevel() == 1 {
		a.utilityScore = a.InitUtility(baseAgent)
		a.uR = a.InitUtility(baseAgent)
		a.uP = a.InitUtility(baseAgent)
		a.uC = a.InitUtility(baseAgent)
	}

	a.AT = int(AS.Attack + AS.BonusAttack())
	a.SH = int(AS.Defense + AS.BonusDefense())

	// a.fightDecisionsHistory = *history

	a.UpdateTotalUtility(baseAgent)
	a.ResetContacts()
	a.UpdateTSN(baseAgent)

	stat := Stats{1, 2, 3, 4}
	a.statsQueue.addStat(stat)
	// fmt.Println("AVG: ", a.statsQueue.averageStats())

	enable := config.EnvToBool("UPDATE_PERSONALITY", true)
	if enable {
		a.UpdatePersonality()
	}
}

func (a *AgentThree) Sanctioning() int {
	return 50
}

func (a *AgentThree) PruneAgentList(agentMap map[commons.ID]agent.Agent) map[commons.ID]agent.Agent {
	// fmt.Println("Agent 3")
	prunned := make(map[commons.ID]agent.Agent)
	for id, agent := range agentMap {
		// Compare to 50 in order to sanction
		toSanctionOrNot := rand.Intn(100)
		if toSanctionOrNot > a.Sanctioning() {
			prunned[id] = agent
		}
	}
	// fmt.Println(len(agentMap))
	// fmt.Println(len(prunned))
	return prunned
}

func (a *AgentThree) UpdatePersonality() {
	a.personality += 1
	// fmt.Println(a.personality)
}

func NewAgentThreeNeutral() agent.Strategy {
	dis, _ := strconv.ParseInt(os.Getenv("PASSIVE_PER"), 10, 0)
	return &AgentThree{
		utilityScore:      CreateUtility(),
		uR:                CreateUtility(),
		uP:                CreateUtility(),
		uC:                CreateUtility(),
		chairTolerance:    0,
		proposalTolerance: make(map[commons.ID]int, 0),
		personality:       int(dis),
		sanctioned:        0,
		statsQueue:        *makeStatsQueue(3),
	}
}

func NewAgentThreePassive() agent.Strategy {
	dis, _ := strconv.ParseInt(os.Getenv("COLLECTIVE_PER"), 10, 0)
	return &AgentThree{
		utilityScore:      CreateUtility(),
		uR:                CreateUtility(),
		uP:                CreateUtility(),
		uC:                CreateUtility(),
		chairTolerance:    0,
		proposalTolerance: make(map[commons.ID]int, 0),
		personality:       int(dis),
		sanctioned:        0,
		statsQueue:        *makeStatsQueue(3),
	}
}
func NewAgentThreeAggressive() agent.Strategy {
	dis, _ := strconv.ParseInt(os.Getenv("SELFISH_PER"), 10, 0)
	return &AgentThree{
		utilityScore:      CreateUtility(),
		uR:                CreateUtility(),
		uP:                CreateUtility(),
		uC:                CreateUtility(),
		chairTolerance:    0,
		proposalTolerance: make(map[commons.ID]int, 0),
		personality:       int(dis),
		sanctioned:        0,
		statsQueue:        *makeStatsQueue(3),
	}
}
