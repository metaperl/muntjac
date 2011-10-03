# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.layouts.LayoutSpacing import (LayoutSpacing,)
from com.vaadin.demo.sampler.features.layouts.HorizontalLayoutBasic import (HorizontalLayoutBasic,)
from com.vaadin.demo.sampler.features.layouts.VerticalLayoutBasic import (VerticalLayoutBasic,)
from com.vaadin.demo.sampler.NamedExternalResource import (NamedExternalResource,)
from com.vaadin.demo.sampler.features.layouts.GridLayoutBasic import (GridLayoutBasic,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class LayoutMargin(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Layout margin'

    def getDescription(self):
        return 'Layouts can have margins on any of the sides. The actual size' + ' of the margin is determined by the theme, and can be' + ' customized using CSS - in this example, the right margin' + ' size is increased.<br/>Note that <i>margin</i>' + ' is the space around the layout as a whole, and' + ' <i>spacing</i> is the space between the components within' + ' the layout.'

    def getRelatedAPI(self):
        return [APIResource(VerticalLayout), APIResource(HorizontalLayout), APIResource(GridLayout)]

    def getRelatedFeatures(self):
        return [LayoutSpacing, HorizontalLayoutBasic, VerticalLayoutBasic, GridLayoutBasic]

    def getRelatedResources(self):
        return [NamedExternalResource('CSS for the layout', self.getThemeBase() + 'layouts/marginexample.css')]