package xiaozhi.modules.agent.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;

/**
 * 智能体内部接口信息DTO
 * 仅包含第三方接口关心的字段：agentName、systemPrompt、ttsModelId、ttsVoiceId
 */
@Data
@Schema(description = "智能体内部接口信息对象")
public class AgentInternalInfoDTO implements Serializable {
    private static final long serialVersionUID = 1L;

    @Schema(description = "智能体名称", example = "客服助手")
    private String agentName;

    @Schema(description = "角色设定参数", example = "你是一个专业的客服助手，负责回答用户问题并提供帮助")
    private String systemPrompt;

    @Schema(description = "语音合成模型标识", example = "tts_model_02")
    private String ttsModelId;

    @Schema(description = "音色标识", example = "voice_02")
    private String ttsVoiceId;
}