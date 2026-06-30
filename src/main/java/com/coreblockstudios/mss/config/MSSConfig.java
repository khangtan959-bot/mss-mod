package com.coreblockstudios.mss.config;

import net.neoforged.neoforge.common.ModConfigSpec;

public class MSSConfig {
    public static final ModConfigSpec.Builder BUILDER = new ModConfigSpec.Builder();
    public static final ModConfigSpec SPEC;

    public static final ModConfigSpec.BooleanValue GENERATE_STRUCTURES;

    static {
        BUILDER.push("generation");
        GENERATE_STRUCTURES = BUILDER
                .comment("Generate More Simple Structures in the world")
                .define("generateStructures", true);
        BUILDER.pop();
        SPEC = BUILDER.build();
    }
}
