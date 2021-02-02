<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology|Labeling" labelsEnabled="1" version="3.4.3-Madeira">
  <renderer-v2 type="singleSymbol" enableorderby="0" symbollevels="0" forceraster="0">
    <symbols>
      <symbol force_rhr="0" clip_to_extent="1" type="line" name="0" alpha="1">
        <layer locked="0" enabled="1" pass="0" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="41,64,237,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.8" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings>
      <text-style blendMode="0" useSubstitutions="0" fontWordSpacing="0" fieldName="'Trecho ' ||  &quot;DC_ID&quot; || ' - ' ||  format_number( &quot;LENGTH&quot; ,2)  || ' m\n'  || &#xd;&#xa; coalesce( 'DN ' ||&quot;DN&quot;, &quot;DIAMETER&quot; ||' mm') ||' - ' ||    format_number(&quot;RESULT_FLO&quot;,2) || ' L/s'" fontWeight="50" fontSizeUnit="Point" multilineHeight="1.5" fontStrikeout="0" fontCapitals="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontFamily="Calibri" fontLetterSpacing="0" isExpression="1" fontSize="9" namedStyle="Regular" textColor="0,0,0,255" textOpacity="1" previewBkgrdColor="#ffffff" fontUnderline="0" fontItalic="0">
        <text-buffer bufferSizeUnits="MM" bufferJoinStyle="64" bufferSize="1" bufferDraw="1" bufferBlendMode="0" bufferColor="240,248,10,255" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferNoFill="0" bufferOpacity="1"/>
        <background shapeType="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeRotation="0" shapeRadiiY="0" shapeFillColor="255,255,255,255" shapeOffsetX="0" shapeBorderWidth="0" shapeRadiiX="0" shapeSizeType="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeX="0" shapeJoinStyle="64" shapeDraw="0" shapeOffsetY="0" shapeBlendMode="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeRadiiUnit="MM" shapeSVGFile="" shapeOffsetUnit="MM" shapeOpacity="1" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSizeUnit="MM" shapeBorderWidthUnit="MM"/>
        <shadow shadowRadius="1.5" shadowColor="0,0,0,255" shadowOffsetAngle="135" shadowRadiusAlphaOnly="0" shadowOpacity="0.7" shadowUnder="0" shadowOffsetDist="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetGlobal="1" shadowRadiusUnit="MM" shadowOffsetUnit="MM" shadowScale="100" shadowBlendMode="6" shadowDraw="0"/>
        <substitutions/>
      </text-style>
      <text-format addDirectionSymbol="0" decimals="0" plussign="0" reverseDirectionSymbol="0" formatNumbers="1" autoWrapLength="0" multilineAlign="1" leftDirectionSymbol="&lt;" rightDirectionSymbol=">" wrapChar="" useMaxLineLengthForAutoWrap="1" placeDirectionSymbol="0"/>
      <placement xOffset="0" fitInPolygonOnly="0" priority="5" repeatDistanceUnits="MM" centroidInside="0" maxCurvedCharAngleIn="20" yOffset="0" distMapUnitScale="3x:0,0,0,0,0,0" distUnits="MM" rotationAngle="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" offsetUnits="MapUnit" quadOffset="4" placementFlags="9" maxCurvedCharAngleOut="-20" dist="0" offsetType="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" repeatDistance="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" centroidWhole="0" placement="2" preserveRotation="1"/>
      <rendering drawLabels="1" obstacleType="0" scaleMax="10000000" displayAll="0" limitNumLabels="0" minFeatureSize="0" obstacle="1" maxNumLabels="2000" fontLimitPixelSize="0" scaleMin="1" fontMaxPixelSize="10000" zIndex="0" scaleVisibility="0" fontMinPixelSize="3" labelPerPart="0" mergeLines="0" obstacleFactor="1" upsidedownLabels="0"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" type="QString" name="name"/>
          <Option name="properties"/>
          <Option value="collection" type="QString" name="type"/>
        </Option>
      </dd_properties>
    </settings>
  </labeling>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerGeometryType>1</layerGeometryType>
</qgis>
