package agent

import (
	"github.com/benbjohnson/immutable"
	"infra/game/commons"
	"infra/game/message"
)

type Trust interface {
	CompileTrustMessage(agentMap *immutable.Map[commons.ID, Agent]) message.Trust
	HandleTrustMessage(message message.TaggedMessage)
}
