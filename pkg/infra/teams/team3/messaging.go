package team3

import (
	"github.com/benbjohnson/immutable"
	"infra/game/agent"
	"infra/game/commons"
	"infra/game/message"
)

func agentInList(agentID commons.ID, messageList []commons.ID) bool {
	for _, id := range messageList {
		if agentID == id {
			return true
		}
	}
	return false
}

// This is where you must compile your trust message. My example implementation takes ALL agents from the agent map **
func (a *AgentThree) CompileTrustMessage(agentMap *immutable.Map[commons.ID, agent.Agent]) (*message.Trust, []commons.ID) {
	// fmt.Println("AGENT 3 COMPOSED: message.Trust")
	// faireness = the function ids --> reputation number: which is the gossip
	num := int(a.samplePercent * float64(agentMap.Len()))
	agentsToMessage := make([]commons.ID, num)

	// Check TSN first
	i := 0
	for _, k := range a.TSN {
		if i == num {
			break
		}
		agentsToMessage[i] = k
		i++
	}

	iterator := agentMap.Iterator()

	for !iterator.Done() {
		k, _, _ := iterator.Next()
		if i == num {
			break
		}

		// try next ID if agent is already being messaged
		if agentInList(k, agentsToMessage) {
			continue
		}

		agentsToMessage[i] = k
		i++
	}

	// declare new trust message

	// avoid concurrent write to/read from trust.Gossip
	repMapDeepCopy := make(map[commons.ID]float64)

	for k, v := range a.reputationMap {
		repMapDeepCopy[k] = v
	}

	// send off
	return message.NewTrust(repMapDeepCopy), agentsToMessage
}

// You will receive a message of type "TaggedMessage"
func (a *AgentThree) HandleTrustMessage(m message.TaggedMessage) {
	// Receive the message.Trust type using m.Message()

	mes := m.Message()
	t := mes.(*message.Trust)

	// Gossip IS reputation map ---> one thread will read it, one thread will write it.
	// Shallow copy introduced in Compile
	iterator := t.Gossip().Iterator()
	for !iterator.Done() {
		id, sentRep, _ := iterator.Next()
		ourRep, exists := a.reputationMap[id]
		if exists {
			diff := ourRep - sentRep
			norm := diff * (a.reputationMap[m.Sender()] / 100.0)
			newRep := ourRep + norm
			a.reputationMap[id] = clampFloat(newRep, 0.0, 100.0)
		} else {
			a.reputationMap[id] = sentRep
		}

	}
	a.socialCap[m.Sender()] += 1
	//fmt.Println("sender is", t.recipients, m.Sender(), a.socialCap[m.Sender()])
	// This function is type void - you can do whatever you want with it. I would suggest keeping a local dictionary

}
