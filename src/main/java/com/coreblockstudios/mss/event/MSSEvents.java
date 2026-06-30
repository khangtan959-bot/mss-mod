package com.coreblockstudios.mss.event;

import com.coreblockstudios.mss.MSS;
import com.coreblockstudios.mss.entity.MSSEntities;
import com.coreblockstudios.mss.entity.custom.*;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;

@EventBusSubscriber(modid = MSS.MODID, bus = EventBusSubscriber.Bus.MOD)
public class MSSEvents {
    @SubscribeEvent
    public static void onEntityAttributes(EntityAttributeCreationEvent event) {
        event.put(MSSEntities.MUMMY.get(), Mummy.createAttributes().build());
        event.put(MSSEntities.SPIRIT.get(), Spirit.createAttributes().build());
        event.put(MSSEntities.QUEEN_SPIDER.get(), QueenSpider.createAttributes().build());
    }
}
