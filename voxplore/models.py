from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any

class SystemInstructionPart(BaseModel):
    text: str

class SystemInstruction(BaseModel):
    parts: List[SystemInstructionPart]

class PrebuiltVoiceConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    voice_name: str = Field(default="puck", alias="voiceName")

class VoiceConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    prebuilt_voice_config: PrebuiltVoiceConfig = Field(default_factory=PrebuiltVoiceConfig, alias="prebuiltVoiceConfig")

class SpeechConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    voice_config: VoiceConfig = Field(default_factory=VoiceConfig, alias="voiceConfig")

class AvatarConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    avatar_name: Optional[str] = Field(default="Kira", alias="avatarName", description="Jay, Paul, Sam, Ingrid, Kira, Vera, Ben, Kai, Leo, Carmen, Piper")
    customized_avatar: Optional[Dict[str, Any]] = Field(default=None, alias="customizedAvatar")

class GenerationConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    response_modalities: List[str] = Field(default=["VIDEO"], alias="responseModalities")
    enable_affective_dialog: Optional[bool] = Field(default=None, alias="enableAffectiveDialog")
    speech_config: Optional[SpeechConfig] = Field(default_factory=SpeechConfig, alias="speechConfig")

class AutomaticActivityDetection(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    disabled: Optional[bool] = False
    start_of_speech_sensitivity: Optional[str] = "START_SENSITIVITY_HIGH"
    end_of_speech_sensitivity: Optional[str] = "END_SENSITIVITY_HIGH"
    prefix_padding_ms: Optional[int] = 20
    silence_duration_ms: Optional[int] = 100

class RealtimeInputConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    automatic_activity_detection: Optional[AutomaticActivityDetection] = Field(default_factory=AutomaticActivityDetection)

class ProactivityConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    proactive_audio: Optional[bool] = True

class FunctionDeclaration(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class Tool(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    function_declarations: Optional[List[FunctionDeclaration]] = Field(default=None, alias="functionDeclarations")

class SetupDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    system_instruction: Optional[SystemInstruction] = Field(default=None, alias="systemInstruction")
    model: str = Field(default="gemini-3.8-live")
    generation_config: GenerationConfig = Field(default_factory=GenerationConfig, alias="generationConfig")
    avatar_config: Optional[AvatarConfig] = Field(default=None, alias="avatarConfig")
    realtime_input_config: Optional[RealtimeInputConfig] = Field(default=None, alias="realtimeInputConfig")
    proactivity: Optional[ProactivityConfig] = Field(default=None)
    tools: Optional[List[Tool]] = None
    input_audio_transcription: Dict[str, Any] = Field(default_factory=dict, alias="inputAudioTranscription")
    output_audio_transcription: Dict[str, Any] = Field(default_factory=dict, alias="outputAudioTranscription")

class SetupMessage(BaseModel):
    setup: SetupDetails

class InlineData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    mime_type: str = Field(alias="mimeType")
    data: str  # Base64 encoded string

class Part(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    text: Optional[str] = None
    inline_data: Optional[InlineData] = Field(default=None, alias="inlineData")

class Content(BaseModel):
    parts: List[Part]
    role: Optional[str] = None

class RealtimeInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    audio: Optional[InlineData] = None
    video: Optional[InlineData] = None
    text: Optional[str] = None

class ClientContent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    turns: List[Content]
    turn_complete: Optional[bool] = Field(default=None, alias="turnComplete")

class FunctionResponse(BaseModel):
    id: Optional[str] = None
    name: str
    response: Dict[str, Any]
    scheduling: Optional[str] = None

class ToolResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    function_responses: List[FunctionResponse] = Field(alias="functionResponses")

class SceneEvent(BaseModel):
    id: Optional[str] = None
    type: str = "event"  # "event" for a user action, "error" for a script error in the scene
    name: Optional[str] = None
    detail: Optional[Any] = None
    message: Optional[str] = None

class PaperRequest(BaseModel):
    url: Optional[str] = None  # an arXiv identifier or a link to the paper
    query: Optional[str] = None  # a title or a description, looked up with Google Search
    name: Optional[str] = None
    data: Optional[str] = None  # an uploaded PDF, Base64 encoded

class ModeRequest(BaseModel):
    preset: Optional[str] = None  # learning or research
    proactive: Optional[bool] = None

class UploadRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str
    mime_type: str = Field(alias="mimeType")
    data: str  # Base64 encoded bytes

class UploadRemove(BaseModel):
    index: int  # position in upload order, from 0

class ClientMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    setup: Optional[SetupDetails] = None
    realtime_input: Optional[RealtimeInput] = Field(default=None, alias="realtimeInput")
    client_content: Optional[ClientContent] = Field(default=None, alias="clientContent")
    tool_response: Optional[ToolResponse] = Field(default=None, alias="toolResponse")
    scene_event: Optional[SceneEvent] = Field(default=None, alias="sceneEvent")  # browser to backend only
    paper_request: Optional[PaperRequest] = Field(default=None, alias="paperRequest")  # browser to backend only
    mode_request: Optional[ModeRequest] = Field(default=None, alias="modeRequest")  # browser to backend only
    upload_request: Optional[UploadRequest] = Field(default=None, alias="uploadRequest")  # browser to backend only
    upload_remove: Optional[UploadRemove] = Field(default=None, alias="uploadRemove")  # browser to backend only

class ModelTurn(BaseModel):
    parts: List[Part]

class Transcription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    text: Optional[str] = None
    finished: Optional[bool] = None
    language_code: Optional[str] = Field(default=None, alias="languageCode")

class ServerContent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    model_turn: Optional[ModelTurn] = Field(default=None, alias="modelTurn")
    turn_complete: Optional[bool] = Field(default=None, alias="turnComplete")
    interrupted: Optional[bool] = None
    input_transcription: Optional[Transcription] = Field(default=None, alias="inputTranscription")
    output_transcription: Optional[Transcription] = Field(default=None, alias="outputTranscription")

class SetupComplete(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

class FunctionCall(BaseModel):
    id: Optional[str] = None
    name: str
    args: Optional[Dict[str, Any]] = None

class ToolCall(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    function_calls: List[FunctionCall] = Field(default_factory=list, alias="functionCalls")

class ToolCallCancellation(BaseModel):
    ids: List[str] = Field(default_factory=list)

class ErrorDetails(BaseModel):
    code: Optional[int] = None
    message: Optional[str] = None
    status: Optional[str] = None

class UsageMetadata(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    prompt_token_count: Optional[int] = Field(default=None, alias="promptTokenCount")
    response_token_count: Optional[int] = Field(default=None, alias="responseTokenCount")
    thoughts_token_count: Optional[int] = Field(default=None, alias="thoughtsTokenCount")
    total_token_count: Optional[int] = Field(default=None, alias="totalTokenCount")

class ServerMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    server_content: Optional[ServerContent] = Field(default=None, alias="serverContent")
    setup_complete: Optional[SetupComplete] = Field(default=None, alias="setupComplete")
    tool_call: Optional[ToolCall] = Field(default=None, alias="toolCall")
    tool_call_cancellation: Optional[ToolCallCancellation] = Field(default=None, alias="toolCallCancellation")
    usage_metadata: Optional[UsageMetadata] = Field(default=None, alias="usageMetadata")
    error: Optional[ErrorDetails] = None

# Messages from the backend to the browser, in addition to the forwarded Live API messages

class GeneratedMediaMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    kind: str  # "image", "video" or "scene" (an HTML document)
    mime_type: str = Field(alias="mimeType")
    data: str  # Base64 encoded bytes
    prompt: Optional[str] = None
    tool: Optional[str] = None
    model: Optional[str] = None
    duration_ms: Optional[int] = Field(default=None, alias="durationMs")
    source_label: Optional[str] = Field(default=None, alias="sourceLabel")  # what a scene was built from
    source_page: Optional[int] = Field(default=None, alias="sourcePage")
    source_image: Optional[str] = Field(default=None, alias="sourceImage")  # that page of the paper, Base64 JPEG

class GenerationStartedMessage(BaseModel):
    id: str
    kind: str
    tool: str
    model: Optional[str] = None
    prompt: Optional[str] = None

class GenerationErrorMessage(BaseModel):
    id: str
    kind: str
    message: str
