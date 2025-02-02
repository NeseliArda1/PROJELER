#include "M261.h"

void SYS_Init(void)
{
    SYS->GPA_MFPH = 0x00000000;
    SYS->GPA_MFPL = SYS_GPA_MFPL_PA7MFP_BPWM1_CH2 | SYS_GPA_MFPL_PA6MFP_BPWM1_CH3 | SYS_GPA_MFPL_PA5MFP_BPWM0_CH5 | SYS_GPA_MFPL_PA4MFP_BPWM0_CH4 | SYS_GPA_MFPL_PA3MFP_BPWM0_CH3 | SYS_GPA_MFPL_PA2MFP_BPWM0_CH2 | SYS_GPA_MFPL_PA1MFP_BPWM0_CH1 | SYS_GPA_MFPL_PA0MFP_BPWM0_CH0;
    SYS->GPB_MFPH = SYS_GPB_MFPH_PB14MFP_EADC0_CH14;
    SYS->GPB_MFPL = 0x00000000;
    SYS->GPC_MFPH = 0x00000000;
    SYS->GPC_MFPL = 0x00000000;
    SYS->GPD_MFPH = 0x00000000;
    SYS->GPD_MFPL = 0x00000000;
    SYS->GPE_MFPH = 0x00000000;
    SYS->GPE_MFPL = 0x00000000;
    SYS->GPF_MFPH = 0x00000000;
    SYS->GPF_MFPL = SYS_GPF_MFPL_PF1MFP_ICE_CLK | SYS_GPF_MFPL_PF0MFP_ICE_DAT;
    SYS->GPG_MFPH = 0x00000000;
    SYS->GPG_MFPL = 0x00000000;
    SYS->GPH_MFPH = 0x00000000;
    SYS->GPH_MFPL = 0x00000000;
    
    return;
}
